import csv
import os

from django.core.management import BaseCommand

from config.settings import BASE_DIR
from unique_content.models import Mineral


class InstantiateCSVError(Exception):
    """
    Exception class for checking the completeness of data in a csv file
    """

    def __init__(self, *args, **kwargs):
        self.message = args[0] if args else 'The file is damaged'

    def __str__(self):
        return self.message


class Command(BaseCommand):
    def handle(self, *args, **options):
        # List of database models to clear
        database_models = [Mineral]
        file_name = 'mineral_labels.csv'

        for model in database_models:
            # Clear the database records for each model
            self.stdout.write(f'Clearing {model.__name__} database...')
            model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Database {model.__name__} cleared successfully.'))

        # Prepare a list of new data
        new_data = []
        try:
            csvfile = open(os.path.join(BASE_DIR, f'unique_content/management/commands/{file_name}'), newline='', encoding='utf-8-sig')
        except FileNotFoundError:
            raise FileNotFoundError(f'{file_name} file is missing')
        else:
            data = csv.DictReader(csvfile)
            print(data.fieldnames)
            if 'abbreviation' in data.fieldnames and 'name_eng' in data.fieldnames and 'name_rus' in data.fieldnames:
                for row in data:
                    new_data.append(
                        {
                            'abbreviation': row['abbreviation'],
                            'name_eng': row['name_eng'],
                            'name_rus': row['name_rus'],
                        }
                    )
            else:
                raise InstantiateCSVError(f"В структуре файла {file_name} не хватает данных")
        finally:
            csvfile.close()

        # Fill the database with new data
        self.stdout.write('Filling "Mineral" database...')
        minerals_for_adding = []
        for mineral in new_data:
            minerals_for_adding.append(Mineral(**mineral))
        print(minerals_for_adding)
        Mineral.objects.bulk_create(minerals_for_adding)
        self.stdout.write(self.style.SUCCESS('"Mineral" database filled successfully.'))
