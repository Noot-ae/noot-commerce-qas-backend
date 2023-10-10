from utils.test import BaseSetup
# Create your tests here.

class TestRating(BaseSetup):
    
    def test_product_rating_list(self):
        response = self.c.get(f"/rating/product/?product={self.product.pk}")
        assert response.status_code == 200, f"{response.content} - {response.status_code} "
        
    def test_product_rating_create(self):
        data = {
            "product" : self.product.pk,
            "rate" : 4,
            "comment" : "really awesome"
        }
        response = self.c.post(f"/rating/product/", data=data, format = 'json', **self.headers, follow=True)
        assert response.status_code == 201, response.content
        