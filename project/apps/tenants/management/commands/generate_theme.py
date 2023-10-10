from django.core.management.base import BaseCommand
from tenants.models.utils import ThemeGenerator

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
              '--theme_name',
               action='store',
               dest='theme',
               type=str,
               default= False,
               help='Theme Name'
        )
        
        parser.add_argument(
              '--delete_all',
               action='store',
               dest='delete_all',
               type=str,
               default= False,
               help='Delete Existing Carousels'
        )

    def handle(self, *args, **options):
        ThemeGenerator(options.get('theme_name', 'commerce')).generate(delete_all=options.get('delete_all', False))