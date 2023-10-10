from django.core.management.base import BaseCommand
from product.factory import ProductFactory
from django.db.transaction import atomic
from user.factory import UserFactory
from category.factory import CategoryFactory

class Command(BaseCommand):

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
              '--size',
               action='store',
               dest='size',
               type=str,
               default= 10,
               help='Size of Objects to be created.'
        )

    def save_objects(self, factory_batch):
        [i.save() for i in factory_batch]

    @atomic
    def handle(self, *args, **options):
        size = int(options['size'])

        CategoryFactory.build_batch(size)

        self.save_objects(
            UserFactory.build_batch(size)
        )

        ProductFactory.build_batch(size)

