from django.db import models


class Menu(models.Model):
    class DisplayLocationChoices(models.TextChoices):
        primary_menu = "primary_menu"
        footer_column_1 = "footer_column_1"
        footer_column_2 = "footer_column_2"
        footer_column_3 = "footer_column_3"
        footer_column_4 = "footer_column_4"
        footer_column_5 = "footer_column_5"
        topbar_1 = "topbar_1"
        topbar_2 = "topbar_2"
        topbar_3 = "topbar_3"
        footer_copy_right_1 = "footer_copy_right_1"
        footer_copy_right_2 = "footer_copy_right_2"
        footer_copy_right_3 = "footer_copy_right_3"


    names = models.ManyToManyField('translations.Translation', blank=True)
    display_location = models.CharField(choices=DisplayLocationChoices.choices, max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, models.CASCADE, related_name="menu_item_set", blank=True, null=True)
    labels = models.ManyToManyField('translations.Translation', blank=True)
    parent_item = models.ForeignKey('self', models.CASCADE, related_name="menu_subitem_set", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey('page.Section', models.CASCADE, blank=True, null=True)
    path = models.CharField(blank=True, null=True, max_length=64)
    is_custom = models.BooleanField(default=False)
    category = models.ForeignKey('category.Category', models.CASCADE, blank=True, null=True, related_name="category_menu_item_set")        

