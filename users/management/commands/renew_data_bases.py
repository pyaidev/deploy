from django.core.management import BaseCommand
from education_content.models import Chapter, Material, MaterialPhotos
from tests.models import Test, Question, QuestionType, Answers, CompletedTest, CompletedQuestion


class Command(BaseCommand):
    def handle(self, *args, **options):
        # List of database models to clear
        database_models = [Chapter, Material, MaterialPhotos, Test, QuestionType, Question, Answers, CompletedTest,
                           CompletedQuestion]

        for model in database_models:
            # Clear the database records for each model
            self.stdout.write(f'Clearing {model.__name__} database...')
            model.objects.all().delete()
            self.stdout.write(self.style.SUCCESS(f'Database {model.__name__} cleared successfully.'))

        # Prepare a list of new data
        new_data = [
            {'title': 'normal'},
            {'title': 'checkbox'},
            {'title': 'radio'},
        ]

        # Fill the database with new data
        self.stdout.write('Filling "QuestionType" database...')
        statuses_for_adding = []
        for status_item in new_data:
            statuses_for_adding.append(QuestionType(**status_item))
        print(statuses_for_adding)
        QuestionType.objects.bulk_create(statuses_for_adding)
        self.stdout.write(self.style.SUCCESS('"QuestionType" database filled successfully.'))
