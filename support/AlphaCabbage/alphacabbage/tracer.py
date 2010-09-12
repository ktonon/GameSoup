import os.path, re, traceback
import unittest


class MethodCall(object):
    
    def __init__(self, obj, method, tb, crop_tb, depth, *args, **kwargs):
        self._obj = obj
        self._method = method
        self.tb_size = len(tb)
        tb = tb[crop_tb:]
        self._tb = filter(lambda x: not x[0].endswith('alphacabbage/tracer.py'), tb)
        self._tb.reverse()
        self._depth = depth
        self._args = args
        self._kwargs = kwargs
        self._result = None
        self._frame = []

    klass = property(lambda self: str(self._obj.__class__.__name__))
    obj = property(lambda self: self._obj)
    method = property(lambda self: self._method.__name__)

    def get_css_classes(self):
        C = []
        # Depth parity
        C.append(self._depth % 2 == 0 and 'even' or 'odd')
        # Test method
        C.append(isinstance(self._obj, unittest.TestCase) and self._method.func_name.startswith('test_') and 'test' or '')
        # Depth
        C.append('depth-%d' % self._depth)
        return ' '.join(C)
    css_classes = property(get_css_classes)
    
    def get_result(self):
        return self._result
    def set_result(self, result):
        self._result = result
    result = property(get_result, set_result)
    
    def get_url(self):
        return u'txmt://open/?url=file://%s&line=%d' % (
            self._method.__code__.co_filename, self._method.__code__.co_firstlineno)
    url = property(get_url)

    def __iter__(self):
        for mc in self._frame:
            yield mc

    def __getitem__(self, index):
        return self._frame[index]

    def append_method_call(self, other):
        self._frame.append(other)
        return len(self._frame) - 1


class TracedError(object):
    
    def __init__(self, e):
        self._e = e
    
    name = property(lambda self: str(self._e.__class__.__name__))
    message = property(lambda self: str(self._e.message))
    
    def __iter__(self):
        pass

    def set_result(self):
        pass

class Tracer(object):
    
    def __init__(self, *objects):
        self._depth = 0
        self._index_path = []
        self._call_trace = MethodCall(self, 'begin_trace', [], 0, -1)
    
    def close(self, Context, get_template):
        t = get_template('tracer/index.html')
        f = open('/Users/kevin/Desktop/ptrace.html', 'w')
        f.write(t.render(Context({
            'frame': self._call_trace
        })))
        f.close()
        
    def tracerize_package(self, module_name):
        def _s(p, dirname, names):
            ppath = '%s%s' % (module_name, p.sub('', dirname).replace('/', '.'))
            for name in names:
                if not name.endswith('.py') or name == '__init__.py': continue
                name = re.sub(r'\.py$', '', name)
                pkg = __import__(ppath, [], [], [name])
                mod = getattr(pkg, name)
                _t(mod)
                
        def _t(module):
            X = module.__dict__.values()
            classes = filter(lambda x: isinstance(x, type) and x.__module__ == module.__name__, X)
            for klass in classes:
                self.tracerize_class(klass)
                
        m = __import__(module_name)
        os.path.walk(m.__path__[0], _s, re.compile(r'^%s' % m.__path__[0]))

    def tracerize_class(self, klass):
        for name, method in klass.__dict__.items():
            # Ignore non-functions and private attributes
            if not hasattr(method, 'func_name') or name.startswith('_'):
                continue
            # Ignore methods that are not defined in the same
            # module as the class
            a = re.match(r'^.*?([^/]+)\.py$', method.__code__.co_filename)
            b = re.match(r'^.*?([^.]+)$', klass.__module__)
            if (a and a.group(1)) != (b and b.group(1)):
                continue
            # Tracerize the method
            setattr(klass, name, self.make_tracer_method(method))

    def make_tracer_method(self, method):
        def _tracer(celf, *args, **kwargs):
            self.down(celf, method, traceback.extract_stack(), *args, **kwargs)
            try:
                return_value = method(celf, *args, **kwargs)
            except Exception, e:
                return_value = None
                self.report_exception(e)
                raise e
            finally:
                self.up(return_value)
            return return_value
        _tracer.__name__ = method.__name__
        return _tracer
    
    def get_parent_frame(self):
        frame = self._call_trace
        for index in self._index_path[:-1]:
            frame = frame[index]
        return frame
        
    def get_frame(self):
        frame = self._call_trace
        for index in self._index_path:
            frame = frame[index]
        return frame
        
    def down(self, celf, method, tb, *args, **kwargs):
        parent_frame = self.get_parent_frame()
        mc = MethodCall(celf, method, tb, parent_frame.tb_size, len(self._index_path), *args, **kwargs)
        frame = self.get_frame()
        i = frame.append_method_call(mc)
        self._index_path.append(i)
    
    def up(self, result):
        frame = self.get_frame()
        frame.set_result(result)
        self._index_path.pop()
    
    def report_exception(self, e):
        te = TracedError(e)
        frame = self.get_frame()
        frame.append_method_call(te)
