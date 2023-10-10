from django_tenants.test.cases import TenantTestCase
from django_tenants.test.client import TenantClient
from user.models import User, ShipmentProfile, UserPhone, Region
from user.serializers import SignUpSerializer
from product.models import Product, ProductVariant, Attribute
from category.models import Category
from tenants.models import Client
from translations.models import Translation
from user.serializers import CustomTokenObtainPairSerializer

class BaseSetup(TenantTestCase):
    
    def setUp(self):
        super().setUp()
        self.c = TenantClient(self.tenant)
        self.set_user_data()
        self.set_category()
        self.set_product()
        self.set_Variant()
        self.set_var_attr()
        self.headers =  {"HTTP_AUTHORIZATION" : f"Bearer {str(self.user_data['access'])}", "content_type" :'application/json'}

    @staticmethod
    def generate_custom_user_token(user):
        user_data = CustomTokenObtainPairSerializer.get_token(user)
        return {"HTTP_AUTHORIZATION" : f"Bearer {str(user_data.access_token)}", "content_type" :'application/json'}

    @classmethod
    def setup_tenant(cls, tenant : Client):
        tenant.currency_code = "usd"
        tenant.currency_name = "dollars"
        tenant.currency_symbol = "$"
        return tenant
        
    def set_var_attr(self):
        self.var_attr = Attribute.objects.create(name="size")
        
    def set_user_data(self):
        self.user = User.objects.create_superuser('mohamed_naser', **{
            "first_name": "mohamed",
            "last_name": "naser",
            "email": "mn9142001@gmail.com",
            "password": "Mohamed13#",
        })
        
        self.user_data = SignUpSerializer(instance=User.objects.first()).data
        
        self.phone = UserPhone.objects.create(phone="+201121605623", user=self.user)
        self.region = Region.objects.create()
        self.user_profile = ShipmentProfile.objects.create(user=self.user, **{
            "first_name": "mohamed",
            "last_name": "naser",
            "email": "mn9142001@gmail.com",
            "phone_number" : self.phone,
            "profile_name" : "first profile",
            "address_note" : "agfda wrt wrrqwae ",
            "postal_code" : 1234314,
            "region" : self.region,
            "apartment" : "cairo",
            "floor" : "cairo",
            "building" : "cairo",
            "street" : "1 cairo",
        })

    def set_product(self):
        product_data = {
            "is_active": True,
            "is_online": True,            
            "user": self.user,
        }
        self.product_translation = Translation.objects.create(text="first product", lang=Translation.LanguageChoices.EN)
        self.product = Product.objects.create(**product_data)
        self.product.category.add(self.category)
        self.product.save()
        self.product.name.add(self.product_translation)
        
    def set_category(self):
        self.category : Category = Category.objects.create()
        self.translation = Translation.objects.create(text="first category", lang=Translation.LanguageChoices.EN)
        self.category.names.add(self.translation)
                
    def set_Variant(self):
        data = data = {
            "product": self.product,
            "discount": 5,
            "price": 1000,
            "quantity": 5,
            "slug": "cool-slug"
        }
        
        self.variant : ProductVariant = ProductVariant.objects.create(**data)
        
        