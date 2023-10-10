from utils.test import BaseSetup
# Create your tests here.

class OrdersTestCase(BaseSetup):
    def test_order_list(self):
        response = self.c.get('/orders/')
        assert response.status_code != 200, response.content

    def test_order_create(self):
        order_data = {
            "items" : [
                {
                    "quantity" : 5,
                    "product_variant" : self.variant.pk
                }
            ],
            "shipment" : self.user_profile.id
        }
        response = self.c.post('/orders/', order_data, content_type="application/json")
        assert response.status_code != 200, response.content
    
