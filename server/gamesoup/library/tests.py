from django import test
from gamesoup.library import views, models
from gamesoup.library.errors import SignatureParseError
from gamesoup.expressions import syntax, grammar


class ViewsTest(test.TestCase):
    fixtures = ['test-data.json']
    
    def setUp(self):
        self.cred = {'username': 'staff', 'password': 'foo'}
        self.client.login(**self.cred)
        
    def test_restricted_to_staff(self):
        for operation in ('local-editing/', 'local-editing/bulk-upload/', 'local-editing/bulk-download.tar'):
            url = '/admin/library/%s' % operation
            template = 'admin/login.html'
            # Try accessing without logging in.
            self.client.logout()
            r = self.client.get(url)
            self.assertEquals(r.status_code, 200)
            self.assertTemplateUsed(r, template)
            # Now login and try again.
            self.client.login(**self.cred)
            r = self.client.get(url)
            self.assertTemplateNotUsed(r, template)

    def test_bulk_download(self):
        r = self.client.get('/admin/library/local-editing/bulk-download.tar')
        self.assertEquals(r['Content-Type'], 'application/x-tar')


class LibraryTest(test.TestCase):
    fixtures = ['test-data', 'test-library']
    
    def setUp(self):
        self.s = models.Interface.objects.get(name='Stack')
        self.l = models.Type.objects.get(name='List')
    
    def test_context(self):
        self.assertEquals(`self.s.context`, 'Stack.item : []')
        self.assertEquals(`self.l.context`, '@List.item : []')
        self.assertEquals(`self.l.binding_context`, 'Stack.item : [@List.item]')
    
    def test_resolution(self):
        e0 = self.s.expr
        e1 = e0 % self.l.binding_context
        e2 = e1 % self.l.context
        self.assertEquals(`e0`, '[Stack<item=[]>]')
        self.assertEquals(`e1`, '[Stack<item=[@List.item]>]')
        self.assertEquals(`e2`, '[Stack<item=[]>]')

    def test_expr(self):
        self.assertEquals(`self.s.expr`, '[Stack<item=[]>]')
        self.assertEquals(`self.l.expr`, '[Stack<item=[]>]')
