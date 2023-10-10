from django.core.exceptions import ValidationError
import json
from product.models import Carousel, Banner
from translations.models import Translation
from page.models import Section
import os
from django.conf import settings
from django.db.transaction import atomic
from django.db.models import Prefetch
from utils.data import default_pages_data
from page.models import Section, Title, SectionContent
    

class ThemeGenerator:
    
    def __init__(self, theme_name) -> None:
        self.theme_name = theme_name
        self.full_theme_path = os.path.join(settings.BASE_DIR, 'themes', f"{theme_name}.json")
        is_file = os.path.isfile(self.full_theme_path)
        if not is_file:
            raise ValidationError("theme name is not valid")


    def delete_all_carousels(self):
        carousels = Carousel.objects.select_related('page').prefetch_related(
            Prefetch('banner_set', Banner.objects.prefetch_related('title', 'sub_title', 'content', 'button_text')), 'page__page_section_set'
        )
        for carousel in carousels:
            for banner in carousel.banner_set.all():
                banner.title.all().delete()
                banner.sub_title.all().delete()
                banner.content.all().delete()
                banner.button_text.all().delete()
                banner.delete()
            carousel.delete()

    @atomic
    def generate(self, delete_all=False):
        if delete_all:
            self.delete_all_carousels()
        self.generate_default_pages()
        self.generate_carousels(self.load_file().get('carousels', []))

    def load_file(self):
        with open(self.full_theme_path, 'r') as file:
            return json.loads(file.read())

    def generate_carousels(self, data):
        for d in data:
            banner_set_data = d.pop("banner_set", [])
            carousel = Carousel.objects.create(
                page=Section.objects.get_or_create(slug=d.pop("page"))[0], 
                **d
            )
            self.generate_banners(banner_set_data, carousel=carousel)

    def generate_translations(self, data : list[dict]):
        for d in data:
            d.pop("id", None)
            d['text'] = ""
        return Translation.objects.bulk_create([Translation(**d) for d in data])

    def generate_banner_translations(self, banner : Banner, translations_data : dict):
        for key in list(translations_data.keys()):
            m2m_field = getattr(banner, key)
            m2m_field.set(
                self.generate_translations(translations_data[key])
            )
        
    def generate_banner(self, data : dict, **kwargs):
        translations_data = {}
        for key in list(data):
            if type(data[key]) == list:
                translations_data[key] = data.pop(key, [])
        
        banner = Banner(**data, **kwargs)
        if "thumbnail" in data:
            banner.thumbnail.name = data['thumbnail']
        banner.save()
        self.generate_banner_translations(banner, translations_data)

    def generate_banners(self, banners_data : list[dict], **extra_kwargs):
        for banner in banners_data:
            self.generate_banner(banner, **extra_kwargs)
  
    @staticmethod
    def generate_default_pages():
        pages = []
        for data in default_pages_data:     
            title_data = data.pop('title_set', [])
            description_data = data.pop("description", [])
            content_data = data.pop("content", [])
            description_objects = SectionContent.objects.bulk_create([SectionContent(**d) for d in description_data])
            content_objects = SectionContent.objects.bulk_create([SectionContent(**d) for d in content_data])
            page = Section.objects.create(**data, section_type=Section.PageSectionType.PAGE)
            page.content.add(*content_objects)
            page.description.add(*description_objects)
            Title.objects.bulk_create([Title(**td, section=page) for td in title_data])
            page.save()
            pages.append(page)
        return pages