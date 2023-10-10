from django.db import models
from ckeditor.fields import RichTextField
from utils.fields import LimitedImageField

# Create your models here.
class LanguageMixin(models.Model):
    class LanguageChoices(models.TextChoices):
        EN = "en"
        AR = "ar"
        
    lang = models.CharField(choices=LanguageChoices.choices, max_length=6, null=True)    
    
    class Meta:
        abstract = True


class Section(models.Model):
    PREFETCH_FIELDS = ['title_set', 'content', 'description']
    FULL_PREFETCH_FIELDS = PREFETCH_FIELDS + ['page_section_set']
    
    is_default = models.BooleanField(default=False)
    slug = models.SlugField(max_length=24, unique=True)
    
    def __str__(self) -> str:
        return self.slug

    class PageSectionType(models.TextChoices):
        PAGE = "Page"
        SECTION = "SECTION"

    section_type = models.CharField(choices=PageSectionType.choices, max_length=16)
    page = models.ForeignKey('self', models.CASCADE, related_name="page_section_set", blank=True, null=True)
    thumbnail = LimitedImageField(blank=True, null=True)
    
    description = models.ManyToManyField('page.SectionContent', blank=True, related_name="description_set")
    content = models.ManyToManyField('page.SectionContent', blank=True, related_name="content_set")


class PageMeta(models.Model):
    page = models.OneToOneField(Section, models.CASCADE, related_name="page_meta")
    keywords = models.CharField(blank=True, null=True, max_length=256)
    description = models.CharField(blank=True, null=True, max_length=256)
    title_tag = models.CharField(blank=True, null=True, max_length=256)
    og_image = models.CharField(blank=True, null=True, max_length=256)
    og_title = models.CharField(blank=True, null=True, max_length=256)
    og_description = models.CharField(blank=True, null=True, max_length=256)


class SectionContent(LanguageMixin, models.Model):
    content = RichTextField(blank=True, null=True)


class Title(LanguageMixin, models.Model):
    class TitleType(models.IntegerChoices):
        TITLE = 0, "Title"
        SUBTITLE = 1, "Sub title"
        
    section = models.ForeignKey(Section, models.CASCADE)
    title = models.CharField(max_length=64, blank=True, null=True)
    title_type = models.IntegerField(choices=TitleType.choices)

    def get_lang_type_display(self):
        return self.lang


class SocialIcon(models.Model):
    
    class IconChoices(models.TextChoices):
        FACEBOOK = "FACEBOOK"
        TWITTER = "TWITTER"
        INSTAGRAM = "INSTAGRAM"
        WHATSAPP = "WHATSAPP"
        
    icon_choice = models.CharField(max_length=32, choices=IconChoices.choices)
    
    def get_icon_url(self):
        return {
            "FACEBOOK" : "",    
            "TWITTER" : "",    
            "INSTAGRAM" : "",    
            "WHATSAPP" : "",    
        }[self.icon_choice]
        
    @property
    def url(self):
        pass