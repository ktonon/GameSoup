'''
For visualizing the products of Expr.parse

Try putting this one into the expression field to see
an example that includes all types of objects.

    [Interable<item=[Readable<item=[]>+Writable<item=[]>]> + Board<cell=item> + Drivable<name=String!, wheel=[]>]

'''
import re
from gamesoup.expressions.syntax import Expr


def render(w, g):
    '''
    Render expression w to graph g.
    '''
    try:
        expr = Expr.parse(w)
    except Exception:
        g.add_node('invalid', label='Could not parse')
        return
    r = Renderer()
    r.add_expr(expr, g)
    return expr


class Renderer(object):

    def __init__(self):
        self._atom = {}
    
    def id_for_atom(self, a, depth, indices):
        if a.is_var:
            id = a.id.replace('@', '').replace('.', '_')
        else:
            id = 'node_%d_%s' % (depth, '_'.join(map(str, indices)))
        return id

    def add_expr(self, e, g, depth=0, indices=None):
        indices = indices or [0]
        id = 'node_%d_%s' % (depth, '_'.join(map(str, indices)))
        node = g.add_node(id, label='')
        node.height = '0.2'
        node.width = '0.2'
        node.style = 'filled'
        node.fillcolor = '#6699cc'
        node.color = '#003366'
        if e.is_var:
            node.shape = 'egg'
            node.color = '#663300'
            node.fillcolor = '#ffcc99'
        if e.is_built_in:
            node.shape = 'hexagon'
            node.color = '#333333'
            node.fillcolor = '#666666'
        atom_indices = list(indices) + [0]
        for i, a in enumerate(e.atoms):
            atom_indices[-1] = i
            atom_node = self.add_atom(a, g, depth=depth+1, indices=atom_indices)
            edge = g.add_edge(node, atom_node)
            edge.color = '#003366'
            if e.is_var:
                edge.color = '#663300'
            if e.is_built_in:
                edge.color = '#333333'
        return node

    def add_atom(self, a, g, depth, indices):
        id = self.id_for_atom(a, depth, indices)
        if id in self._atom:
            return self._atom[id]
        else:
            label = a.id
            node = g.add_node(id, label=label)
            self._atom[id] = node
        if a.is_var:
            node.style = 'filled'
            node.color = '#ffcc99'
            node.fillcolor = '#ffcc99'
            node.fontcolor = '#663300'
            node.shape = 'egg'
        if a.is_built_in:
            node.style = 'filled'
            node.color = '#333333'
            node.fillcolor = '#333333'
            node.fontcolor = 'white'
            node.shape = 'hexagon'
        arg_indices = list(indices) + [0]
        for i, arg in enumerate(a.args):
            arg_indices[-1] = i
            arg_node = self.add_arg(arg, g, depth=depth+1, indices=arg_indices)
            edge = g.add_edge(node, arg_node)
            edge.color = '#666666'
            edge.arrowhead = 'none'
            
        return node

    def add_arg(self, arg, g, depth, indices):
        id = 'node_%d_%s' % (depth, '_'.join(map(str, indices)))
        label = arg.id
        node = g.add_node(id, label=label)
        node.shape = 'invhouse'
        node.height = '0.5'
        node.width = '0.5'
        node.style = 'filled'
        node.fillcolor = '#e8e8e8'
        node.fontcolor = '#666666'
        node.color = "#666666"
        expr_node = self.add_expr(arg.expr, g, depth=depth+1, indices=indices + [0])
        edge = g.add_edge(node, expr_node)
        edge.color = "#666666"
        edge.arrowhead = 'none'
        return node
