from django.db import models

# Create your models here.
class Translation(models.Model):

    class LanguageChoices(models.TextChoices):
        EN = "en"
        AR = "ar"

    is_ltr = models.BooleanField(default=True)
    lang = models.CharField(choices=LanguageChoices.choices, max_length=6)
    text = models.TextField(max_length=5048, blank=True, null=True)

    def get_lang_type_display(self):
        return self.lang

    def __str__(self) -> str:
        return f"{self.id} - {self.get_lang_type_display()}"