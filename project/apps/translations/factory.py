import factory
from translations.models import Translation
from factory import fuzzy

class TranslationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Translation

    lang = fuzzy.FuzzyChoice(Translation.LanguageChoices)
    text = factory.Faker("profile")
    