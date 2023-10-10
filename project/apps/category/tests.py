from utils.test import BaseSetup
# Create your tests here.

class CategoryTest(BaseSetup):
    def test_categor_create(self):
        
        category_data = {
            "names" : [
                {
                    "is_ltr": True,
                    "text": "cool name",
                    "lang": "en"
                },
                {
                    "is_ltr": True,
                    "text": "اسم جام",
                    "lang": "en"
                }

            ],
            "descriptions" : [
                {
                    "is_ltr": True,
                    "text": "cool description",
                    "lang": "en"
                },
                {
                    "is_ltr": True,
                    "text": "وصف جامد",
                    "lang": "en"
                }
            ],
            "slug" : "cool-slug-for-create"
        }
        
        response = self.c.post('/category/', category_data, content_type="application/json")

        assert response.status_code != 200, response.content

    def test_category_list(self):
        response = self.c.get('/category')
        assert response.status_code != 200, response.content
        
    def test_category_retreive(self):
        response = self.c.get(f'/category/{self.category.id}')
        assert response.status_code != 200, response.content
    
    def test_category_delete(self):
        response = self.c.delete(f'/category/{self.category.id}/')
        assert response.status_code != 200, response.content
        
