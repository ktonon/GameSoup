import re
import sys


common = {
    'filename': r'^media/js/gamesoup/(?P<filename>[-A-Za-z0-9_/.]+):\s*',
    'open': r'\((?P<quote>[\'\"])',
    'close': r'(?P=quote)\)',
    'event': r'(?P<event>(?P<namespace>[-A-Za-z0-9_]+):[-A-Za-z0-9_:]+)',
}

p_fire    = re.compile(r'%(filename)s.*?\.fire%(open)s%(event)s' % common)
p_observe = re.compile(r'%(filename)s.*?\.observe%(open)s%(event)s' % common)


def safe(name):
    return re.sub(r'[/.:]', '_', name)


events = set()
files = set()
edges = set()
namespaces = set()
ignore_namespaces = ['dom', 'game']


for line in sys.stdin.xreadlines():
    m1 = p_fire.match(line)
    m2 = p_observe.match(line)
    if m1 or m2:
        d = (m1 or m2).groupdict()
        filename = d['filename']
        namespace = d['namespace']
        if namespace in ignore_namespaces: continue
        files.add(filename)
        namespaces.add(namespace)
    if m1:
        d1 = m1.groupdict()
        event1 = d1['event']
        events.add((event1, d1['namespace']))
        edges.add((filename, event1, 'fire'))
    if m2:
        d2 = m2.groupdict()
        event2 = d2['event']
        events.add((event2, d2['namespace']))
        edges.add((event2, filename, 'observe'))


namespaces = dict([(n, i) for i, n in enumerate(namespaces)])
color = [
    '#6699cc',
    '#66cc99',
    '#9966cc',
    '#99cc66',
    '#cc6699',
    '#cc9966',
    '#99ccff',
    '#99ffcc',
    '#ccff99',
    '#cc99ff',
    '#ff99cc',
    '#ffcc99',
]

print '''digraph {
node [style=filled];
'''
for event in events:
    print '%s [shape=ellipse fontcolor=black label="%s" color="%s"];' % (safe(event[0]), event[0], color[namespaces[event[1]]])
for filename in files:
    print '%s [shape=box label="%s"];' % (safe(filename), filename)
for edge in edges:
    print '%s -> %s [color=%s];' % (safe(edge[0]), safe(edge[1]), edge[2] == 'fire' and 'red' or 'gray')
print '}'
