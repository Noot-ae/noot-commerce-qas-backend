from utils.test import BaseSetup

# Create your tests here.
class TranslationTestCase(BaseSetup):

    def test_search(self):
        """Animals that can speak are correctly identified"""
        response = self.c.get('/translations/search/', {'q': 'backbag'})
        assert response.status_code < 500, response.content
        
    
    def test_translation_update(self):
        data = {
            "text" : "translation is working god damn right"
        }
        response = self.c.patch(f'/translations/update/{self.product_translation.id}/{self.product.id}/', data, format = 'json', **self.headers, follow=True)
        assert response.status_code == 200, response.content

    def test_translate(self):
        data = {
            "text" : "translation is working god damn right",
            "destination" : "english"
        }
        response = self.c.post(f'/translations/', data=data, format = 'json', **self.headers, follow=True)
        assert response.status_code == 200, response.content
