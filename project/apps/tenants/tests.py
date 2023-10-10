from utils.test import BaseSetup
from user.models import User
from django.conf import settings

# Create your tests here.

class TenantTest(BaseSetup):
    
    def test_get_currency(self):
        response = self.c.get(f'/tenants/currency', **self.headers, follow=True)
        assert response.status_code < 400, response.content

    # def test_create_tenant(self):
    #     data = {
    #         "allow_purchase": True,
    #         "currency_code": "USD",
    #         "currency_factor": 1,
    #         "currency_name": "Dollar",
    #         "currency_symbol": "$",
    #         "domain": {
    #             "domain": "electronics-ecommerce.apexcode.info",
    #             "is_primary": False
    #         },
    #         "is_enabled": True,
    #         "minimum_order_price": 10,
    #         "theme_name": "commerce",
    #         "user": {
    #             "email": "test@gmail.com",
    #             "first_name": "test",
    #             "last_name": "test",
    #             "password1": "testPass13#",
    #             "password2": "testPass13#",
    #             "username": "electronics-ecommerce.apexcode.info"
    #         },
    #         "username": "electronics-ecommerce.apexcode.info"
    #     }
    #     response = self.c.post(f"/tenants/", data, **self.generate_custom_user_token(self.tenant_handler_user), follow=True)
    #     print("response here", response.content)
    #     assert response.status_code < 400, response.content

    @property
    def tenant_handler_user(self):
        return User.objects.get_or_create(username=settings.TENANT_HANDLER_USERNAME, password="reallyDummyText")[0]