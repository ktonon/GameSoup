import re
import sys
from common import color, safe

DEFAULT_PACKAGE = 'gamesoup'

common = {
    'filename': r'gamesoup/(?P<importer_app_name>[A-Za-z0-9_]+)/(?P<importer_module_path>[/.A-Za-z0-9_]+)\.py:\s*',
    'package': r'(?P<package>[A-Za-z0-9_]+)',
    'app_name': r'(?P<app_name>[A-Za-z0-9_]+)',
    'module': r'(?P<module>[.A-Za-z0-9_]+)',
    'imported': r'(?P<imported>[*, A-Za-z0-9_]+)',
    'comment': r'\s*(?:\#.*)?',
}

# import gamesoup.library.models
p_import = re.compile(r'^%(filename)simport\s+%(package)s\.%(app_name)s\.%(module)s%(comment)s$' % common)

# from gamesoup.library import models
p_from1 = re.compile(r'^%(filename)sfrom\s+%(package)s\.%(app_name)s\s+import\s+%(imported)s%(comment)s$' % common)

# from gamesoup.library.models import *
p_from2 = re.compile(r'^%(filename)sfrom\s+%(package)s\.%(app_name)s\.%(module)s\s+import\s+%(imported)s%(comment)s$' % common)

# from models import *
p_from3 = re.compile(r'^%(filename)sfrom\s+%(module)s\s+import\s+%(imported)s%(comment)s$' % common)


def path2name(path):
    return path.replace('/', '.')


class Manager(object):
    
    def dot_kwargs(self):
        return u' '.join([u'%s="%s"' % (k, v)
            for k,v in self._kwargs.items()])

    @classmethod
    def create(cls, *args, **kwargs):
        if not hasattr(cls, 'objects'):
            cls.objects = {}
            cls._ids = []
        obj = cls(*args, **kwargs)
        if obj.id not in cls.objects:
            cls.objects[obj.id] = obj
            cls._ids.append(obj.id)
        else:
            obj = cls.objects[obj.id]
        return obj
    

class App(Manager):
    
    def __init__(self, package, app_name, **kwargs):
        self._package = package
        self._app_name = app_name
        self._kwargs = kwargs
    
    def get_id(self):
        return u'%s__dot__%s' % (self._package, self._app_name)
    id = property(get_id)

    def get_color(self):
        return color[self.__class__._ids.index(self.id)]
    color = property(get_color)
    

class Module(Manager):
    
    def __init__(self, package, app_name, module, **kwargs):
        self._app = App.create(package, app_name)
        self._module = path2name(module)
        self._kwargs = kwargs
    
    def get_id(self):
        return u'%s__dot__%s' % (self._app.id, self._module.replace('.', '_'))
    id = property(get_id)
    
    def get_label(self):
        return u'%s' % self._module
    label = property(get_label)
    
    def as_dot(self):
        return u'%s [label="%s" color="%s" %s]' % (self.id, self.label, self._app.color, self.dot_kwargs())


class Edge(Manager):
    
    def __init__(self, mod1, mod2, **kwargs):
        self._mod1 = mod1
        self._mod2 = mod2
        self._kwargs = kwargs
    
    def get_id(self):
        return u'%s__to__%s' % (self._mod1.id, self._mod2.id)
    id = property(get_id)

    def as_dot(self):
        return u'%s -> %s [%s]' % (self._mod1.id, self._mod2.id, self.dot_kwargs)

    
for line in sys.stdin.xreadlines():
    m_import = p_import.match(line)
    m_from1 = p_from1.match(line)
    m_from2 = p_from2.match(line)
    m_from3 = p_from3.match(line)
    m = m_import or m_from1 or m_from2 or m_from3
    if m:
        d = m.groupdict()
        package = d.get('package', DEFAULT_PACKAGE)
        if package not in ['gamesoup']:
            continue
        importer_package = DEFAULT_PACKAGE
        importer_app_name = d['importer_app_name']
        importer_module = d['importer_module_path']
        importer = Module.create(importer_package, importer_app_name, importer_module)
        app_name = d.get('app_name', importer_app_name)
    
    m = m_import or m_from2 or m_from3
    if m:
        module = m.groupdict()['module']
        if module.split('.')[0] in ['gamesoup', 'django', 'cStringIO']:
            continue
        imported = Module.create(package, app_name, module)
        Edge.create(importer, imported)
    elif m_from1:
        modules = m_from1.groupdict()['imported']
        for module in modules.split(','):
            module = module.strip()
            if module in ['*']:
                continue
            imported = Module.create(package, app_name, module)
            Edge.create(importer, imported)


print '''digraph {
node [style=filled];
'''

for mod in Module.objects.values():
    print mod.as_dot()

for edge in Edge.objects.values():
    print edge.as_dot()

print '}'

# namespaces = dict([(n, i) for i, n in enumerate(namespaces)])
# 
# print '''digraph {
# node [style=filled];
# '''
# for event in events:
#     print '%s [shape=ellipse fontcolor=black label="%s" color="%s"];' % (safe(event[0]), event[0], color[namespaces[event[1]]])
# for filename in files:
#     print '%s [shape=box label="%s"];' % (safe(filename), filename)
# for edge in edges:
#     print '%s -> %s [color=%s];' % (safe(edge[0]), safe(edge[1]), edge[2] == 'fire' and 'red' or 'gray')
# print '}'
