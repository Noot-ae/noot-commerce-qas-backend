import factory
from .models import User
import random
from string import ascii_letters

FAKER = factory.Faker("paragraph")

class UserFactory(factory.django.DjangoModelFactory):
    
    avatar = factory.django.ImageField(color='red')
    username = factory.Sequence(lambda x : f"sluggy-{x}-{''.join(random.choices(ascii_letters, k=5))}")
    first_name = factory.Sequence(lambda n: "Agent %03d" % n)
    last_name = factory.Sequence(lambda n: "Agent %03d" % n)
    email = factory.Sequence(lambda n: f"me_{''.join(random.choices(ascii_letters, k=5))}@gmail.com")
    password = factory.django.Password('pw')
    
    
    class Meta:
        model = User
    

