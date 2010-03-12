'''Utility functions.

Functions:
    import_module_from_path    
'''


def import_module_from_path(path):
    '''Import a module given a full path.
 
    raises::
        ImportError
    '''
    i = path.rfind('.')
    pkg_name = str(path[:i])
    mod_name = str(path[i+1:])
    pkg = __import__(pkg_name, globals(), locals(), [mod_name])
    return getattr(pkg, mod_name)