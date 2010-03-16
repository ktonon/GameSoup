'''
Local editing allows developers the ability to upload
and download Type.code as tar files. This module provides
functions for packing and unpacking these files to and
from the database.
'''


import os
import os.path
import shutil
import subprocess
from django.conf import settings
from gamesoup.library.models import *


__all__ = [
    'pack_types',
    'unpack_types',
]


def pack_types(username, outfile):
    user_dir, tar_file = _get_paths(username)
    os.mkdir(user_dir)

    # Write the files
    def make_file(type, field, extension):
        path = os.path.join(user_dir, '%s.%s' % (type.name, extension))
        f = open(path, 'w')
        f.write(getattr(type, field))
        f.close()            
    for type in Type.objects.all():
        make_file(type, 'code', 'js')
    
    # Tar them and read the tarred file into the outfile
    os.chdir(settings.LOCAL_EDITING_WORKSPACE)
    subprocess.call(['tar', '-cf', tar_file, username])
    f = open(tar_file)
    outfile.write(f.read())
    f.close()
    
    # Cleanup the workspace
    os.remove(tar_file)
    shutil.rmtree(user_dir)
    return 


def unpack_types(username, tarball):
    messages = []
    user_dir, tar_file = _get_paths(username)
    
    f = open(tar_file, 'w')
    f.write(tarball.read())
    f.close()
    
    os.chdir(settings.LOCAL_EDITING_WORKSPACE)
    
    return_code = subprocess.call(['tar', '-xf', tar_file])
    if return_code != 0:
        raise ValueError('Invalid file format. Attempt to untar uploaded file failed.')
    
    pattern = re.compile(r'^(?P<type_name>[^.]+)\.(?P<ext>css|js|html)$')
    fieldmap = {
        'css': 'style',
        'js': 'code',
        'html': 'body',
    }
    for filepath in os.listdir(user_dir):
        match = pattern.match(filepath)
        if match:
            d = match.groupdict()
            type_name = d['type_name']
            field = fieldmap[d['ext']]
            f = open(os.path.join(username, filepath))
            try:
                type = Type.objects.get(name=type_name)
                setattr(type, field, f.read())
                type.save()
                messages.append('<strong>%s</strong>.<em>%s</em> updated...' % (type_name, field))
            except Type.DoesNotExist:
                messages.append('Unknown type <strong>%s</strong> for file <em>%s</em>' % (type_name, filepath))
            f.close()
        else:
            messages.append('Unrecognized file <em>%s</em>' % filepath)

    # Cleanup the workspace
    os.remove(tar_file)
    shutil.rmtree(user_dir)
    return messages

    
###############################################################################
# LOCAL HELPERS


def _get_paths(username):
    user_dir = os.path.join(settings.LOCAL_EDITING_WORKSPACE, username)
    tar_file = '%s.tar' % username
    return user_dir, tar_file