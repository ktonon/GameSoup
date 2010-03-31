from django import test
from gamesoup.library import views, models
from gamesoup.library.errors import SignatureParseError
from gamesoup.library import templation


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


class ExpressionTest(test.TestCase):
    fixtures = ['test-data.json', 'test-expressions.json']

    def setUp(self):
        self.any = models.Interface.objects.any()
        self.string = models.Interface.objects.get(name='String')
        self.action = models.Interface.objects.get(name='Action')
        self.iterable = models.Interface.objects.get(name='Iterable')
        self.readwrite = models.Interface.objects.get(name='ReadWrite')
    
    def test_atomic_expression_parsing(self):
        e = templation.InterfaceExpression('Any')
        self.assertEquals(e.interface, self.any)
        e = templation.InterfaceExpression('String')
        self.assertEquals(e.interface, self.string)
        e = templation.InterfaceExpression('Action')
        self.assertEquals(e.interface, self.action)

    def test_expression_parsing_one_level(self):
        e = templation.InterfaceExpression('Iterable<Item=String>')
        self.assertEquals(e.interface, self.iterable)
        self.assertEquals(e['Item'].interface, self.string)

    def test_expression_parsing_deep(self):
        e = templation.InterfaceExpression('Iterable<Item=ReadWrite<Item=String>>')
        self.assertEquals(e.interface, self.iterable)
        self.assertEquals(e['Item'].interface, self.readwrite)
        self.assertEquals(e['Item']['Item'].interface, self.string)

    def test_simple_expression_compare(self):
        any = templation.InterfaceExpression('Any')
        readable = templation.InterfaceExpression('Readable')
        writable = templation.InterfaceExpression('Writable')
        # readwrite = templation.InterfaceExpression('Readable & Writable')
        self.assertTrue(any == any)
        self.assertTrue(readable == readable)
        self.assertTrue(any != readable)        
        self.assertTrue(any > readable)
        self.assertTrue(readable < any)
        self.assertTrue(any > writable)
        # self.assertTrue(any > readwrite)
        # self.assertTrue(readable > readwrite)
        # self.assertTrue(writable > readwrite)
        # self.assertFalse(readable < readwrite)
        # self.assertFalse(writable < readwrite)

    def test_complex_expression_compare(self):
        readable = templation.InterfaceExpression('Readable')
        readable_string = templation.InterfaceExpression('Readable<Item=String>')
        # readwrite_string = templation.InterfaceExpression('ReadWrite<Item=String>')
        self.assertTrue(readable != readable_string)
        self.assertTrue(readable > readable_string)
        self.assertFalse(readable < readable_string)
        # self.assertTrue(readable > readwrite_string)
        # self.assertTrue(readable_string > readwrite_string)

    def test_very_complex_expression_compare(self):
        any = templation.InterfaceExpression('Any')
        string = templation.InterfaceExpression('String')
        readwrite = templation.InterfaceExpression('ReadWrite')
        factory = templation.InterfaceExpression('Factory')
        special_factory_a = templation.InterfaceExpression('Factory<Item=Readable<Item=Any>>')
        # special_factory_b = templation.InterfaceExpression('Factory<Item=ReadWrite<Item=String>>')
        self.assertTrue(factory > special_factory_a)
        # self.assertTrue(factory > special_factory_b)
        self.assertTrue(any > factory)
        self.assertTrue(any > special_factory_a)
        # self.assertTrue(any > special_factory_b)
        # self.assertFalse(string > special_factory_b)
        # self.assertFalse(readwrite > special_factory_b)
        # self.assertTrue(special_factory_a > special_factory_b)


__test__ = {'doctest': 
    templation.__test__['doctest'],
}
