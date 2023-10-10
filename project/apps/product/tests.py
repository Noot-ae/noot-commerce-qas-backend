from utils.test import BaseSetup


# Create your tests here.
class ProductTestCase(BaseSetup):

    def test_product_create(self):
        data = {
            "items": [
                {
                    "price": 150,
                    "name" : "used",            
                    "price": 220,
                    "quantity" : 5
                }
            ],
            "is_active": True,
            "is_online": True,
            "name": [
                        {"text" : "Cool backbag", "lang" : "en"},
                        {"text" : "شنطة", "lang" : "ar", "is_ltr" : False}
            ],
            "description": [
                {"text" : "That is a really fine peice of backbag", "lang" : "en"},
                {"text" : "شنطة رايقة", "lang" : "ar"}
            ],
            "category": [self.category.pk]
        }
        
        response = self.c.post('/products/create/', data, format = 'json', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    def test_product_update(self):
        data = {
            "is_active": True,
            "is_online": True,
            "quantity" : 5,
            "category": [self.category.pk]
        }
        response = self.c.patch(f'/products/change/{self.product.pk}/', data, format = 'json', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    def test_variant_create(self):
        data = {
            "variant_attribute_set": [],
            "images_set": [],
            "product": self.product.pk,
            "discount": 5,
            "price": 1000,
            "quantity": 47483648,
            "slug": "coosl-slug"
        }
        
        response = self.c.post(f'/products/variant/', data, format = 'json', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    def test_variant_update(self):
        data = {
            "discount": 3,
            "price": 1000,
            "quantity": 500,
        }
        
        response = self.c.patch(f'/products/variant/{self.variant.pk}/', data, format = 'json', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    def test_variant_attr_create(self):
        data = {
            "category": self.category.pk,
            "name": "size",
        }
        
        response = self.c.post(f'/products/variants/attribute/', data, format = 'json', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    def test_variant_variant_attribute_set(self):
        data = {
            "variant_attribute_set" : [
                {
                    "attribute" : self.var_attr.pk,
                    "attribute_value" : "3XL"
                }
            ],
            "product_variant" : self.variant.id
        }
        
        response = self.c.post(f'/products/variants/attribute/', data, format = 'json', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    def test_product_get(self):
        response = self.c.get(f'/products', **self.headers, follow=True)
        assert response.status_code < 400, response.content

    def test_product_delete(self):
        response = self.c.delete(f'/products/variants/change/{self.variant.pk}/', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    def test_product_delete(self):
        response = self.c.delete(f'/products/change/{self.product.pk}/', **self.headers, follow=True)
        assert response.status_code < 400, response.content
        
    