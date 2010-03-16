from django import test
from gamesoup.library import views, models


class ViewsTest(test.TestCase):
    fixtures = ['test-auth.json', 'test-library.json']
    
    def setUp(self):
        self.cred = {'username': 'staff', 'password': 'foo'}
        self.client.login(**self.cred)
        
    def test_restricted_to_staff(self):
        for operation in ('local-editing/bulk-upload', 'local-editing/bulk-download'):
            url = '/admin/library/%s/' % operation
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
        r = self.client.get('/admin/library/local-editing/bulk-download/')
        self.assertEquals(r['Content-Type'], 'application/x-tar')