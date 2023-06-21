import csv

from django.core.management import BaseCommand

from .serializers_for_import import IngredientSerializer


class Command(BaseCommand):
    """Managa command for importing ingredients."""

    help = 'Adds ingredients to your database.'

    def handle(self, *args, **options):
        try:
            with open('data/ingredients.csv', encoding="utf8") as csv_file:
                reader = csv.DictReader(csv_file)
                for row_dict in reader:
                    serializer = IngredientSerializer(data=row_dict)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        self.stdout.write(self.style.ERROR(
                            'Ошибка в файле ingredients.csv\n'
                            f'{serializer.errors} {row_dict}'
                        ))

                self.stdout.write(self.style.SUCCESS(
                    'Файл ingredients.csv успешно загружен в базу'
                ))
        except Exception as e:
            raise Exception(f'Ошибка {e}')
