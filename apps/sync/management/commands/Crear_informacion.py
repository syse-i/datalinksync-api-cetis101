from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from apps.data.models import Data


class Command(BaseCommand):
    help = """
    Se genera informacion de prueba Data
    """

    def handle(self, *args, **options):
        
        faker = Faker()
        for cant in range(100):
            try:
                Data.objects.create(name=faker.first_name(), last_name=faker.last_name(), number_phone='8109203243')
            except Exception as e:
                pass
        return print('Successfully')
