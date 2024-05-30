import csv
import os

from django.core.management import BaseCommand

from config.settings import BASE_DIR
from unique_content.models import Label, FigureThinSection, Mineral


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
        database_models = [Label]
        file_name = 'labels.csv'

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
            if 'figure_thin_section' in data.fieldnames and 'mineral' in data.fieldnames and 'coord_X' in data.fieldnames and 'coord_Y' in data.fieldnames:
                for row in data:
                    new_data.append(
                        {
                            'figure_thin_section': FigureThinSection.objects.get(pk=row['figure_thin_section']),
                            'mineral': Mineral.objects.get(pk=row['mineral']),
                            'coord_X': row['coord_X'],
                            'coord_Y': row['coord_Y'],
                        }
                    )
            else:
                raise InstantiateCSVError(f"В структуре файла {file_name} не хватает данных")
        finally:
            csvfile.close()

        # Fill the database with new data
        self.stdout.write('Filling "Label" database...')
        labels_for_adding = []
        for mineral in new_data:
            labels_for_adding.append(Label(**mineral))
        print(labels_for_adding)
        Label.objects.bulk_create(labels_for_adding)
        self.stdout.write(self.style.SUCCESS('"Label" database filled successfully.'))
