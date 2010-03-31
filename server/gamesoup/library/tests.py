from django import test
from gamesoup.library import views, models
from gamesoup.library.errors import SignatureParseError
from gamesoup.library.expressions import syntax, semantics


class ViewsTest(test.TestCase):
    fixtures = ['test-data.json', 'test-library.json']
    
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


class ExpressionSyntaxTest(test.TestCase):
    fixtures = ['test-data.json', 'test-expressions.json']

    def setUp(self):
        self.any = models.Interface.objects.any()
        self.string = models.Interface.objects.get(name='String')
        self.action = models.Interface.objects.get(name='Action')
        self.iterable = models.Interface.objects.get(name='Iterable')
        self.readable = models.Interface.objects.get(name='Readable')
        self.writable = models.Interface.objects.get(name='Writable')
    
    def test_atomic_expression_parsing(self):
        e = semantics.InterfaceExpression.parse('Any')
        self.assertEquals(e[0].interface, self.any)
        e = semantics.InterfaceExpression.parse('String')
        self.assertEquals(e[0].interface, self.string)
        e = semantics.InterfaceExpression.parse('Action')
        self.assertEquals(e[0].interface, self.action)

    def test_expression_parsing_one_level(self):
        e = semantics.InterfaceExpression.parse('Iterable<item=String>')
        self.assertEquals(e[0].interface, self.iterable)
        self.assertEquals(e[0]['item'][0].interface, self.string)

    def test_expression_parsing_deep(self):
        e = semantics.InterfaceExpression.parse('Iterable<item=Readable<item=String>>')
        self.assertEquals(e[0].interface, self.iterable)
        self.assertEquals(e[0]['item'][0].interface, self.readable)
        self.assertEquals(e[0]['item'][0]['item'][0].interface, self.string)

    def test_simple_expression_compare(self):
        any = semantics.InterfaceExpression.parse('Any')
        readable = semantics.InterfaceExpression.parse('Readable')
        writable = semantics.InterfaceExpression.parse('Writable')
        # readwrite = semantics.InterfaceExpression.parse('Readable & Writable')
        # self.assertTrue(any == any)
        # self.assertTrue(readable == readable)
        # self.assertTrue(any != readable)        
        # self.assertTrue(any > readable)
        # self.assertTrue(readable < any)
        # self.assertTrue(any > writable)
        # self.assertTrue(any > readwrite)
        # self.assertTrue(readable > readwrite)
        # self.assertTrue(writable > readwrite)
        # self.assertFalse(readable < readwrite)
        # self.assertFalse(writable < readwrite)

    def test_complex_expression_compare(self):
        readable = semantics.InterfaceExpression.parse('Readable')
        readable_string = semantics.InterfaceExpression.parse('Readable<item=String>')
        # readwrite_string = semantics.InterfaceExpression.parse('ReadWrite<item=String>')
        # self.assertTrue(readable != readable_string)
        # self.assertTrue(readable > readable_string)
        # self.assertFalse(readable < readable_string)
        # self.assertTrue(readable > readwrite_string)
        # self.assertTrue(readable_string > readwrite_string)

    def test_very_complex_expression_compare(self):
        any = semantics.InterfaceExpression.parse('Any')
        string = semantics.InterfaceExpression.parse('String')
        factory = semantics.InterfaceExpression.parse('Factory')
        special_factory_a = semantics.InterfaceExpression.parse('Factory<item=Readable<item=Any>>')
        # special_factory_b = semantics.InterfaceExpression.parse('Factory<item=ReadWrite<item=String>>')
        # self.assertTrue(factory > special_factory_a)
        # self.assertTrue(factory > special_factory_b)
        # self.assertTrue(any > factory)
        # self.assertTrue(any > special_factory_a)
        # self.assertTrue(any > special_factory_b)
        # self.assertFalse(string > special_factory_b)
        # self.assertFalse(readwrite > special_factory_b)
        # self.assertTrue(special_factory_a > special_factory_b)

    def test_nested_expression_set(self):
        e = semantics.InterfaceExpression.parse('Iterable<item=[Readable<item=String> & Writable<item=String>]>')
        self.assertEquals(e[0]['item'][0].interface, self.readable)
        self.assertEquals(e[0]['item'][1].interface, self.writable)
        self.assertEquals(e[0]['item'][1]['item'][0].interface, self.string)


__test__ = {'doctest': 
    '\n'.join([
        syntax.__test__['doctest'],
        semantics.__test__['doctest'],
        ])
}
