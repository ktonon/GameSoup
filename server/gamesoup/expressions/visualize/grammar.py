'''
For visualizing the products of Rule.expr
'''
from gamesoup.expressions.grammar import Rule


def render(w, g):
    '''
    Render expression w to graph g.
    '''
    try:
        tree = Rule.expr(w)
    except Exception, e:
        g.add_node('invalid', label='%s' % e)
        return
    _add_tuple(tree, g)
    return tree


def _add_tuple(t, g, depth=0, index=0):
    label = t[0]
    id = 'node_%d_%d' % (depth, index)
    node = g.add_node(id, label=label)
    if label == 'EXPR':
        node.style = 'filled'
        node.fillcolor = '#6699cc'
    for i, child in enumerate(t[1:]):
        if isinstance(child, tuple):
            childNode = _add_tuple(child, g, depth=depth+1, index=i)
        else:
            child_id = 'node_%d_%d' % (depth+1, i)
            childNode = g.add_node(child_id, label=child)
            childNode.shape = 'box'
            childNode.style = 'filled'
            childNode.fontcolor = 'white'
            childNode.fillcolor = '#333333'
        g.add_edge(node, childNode)
    return node