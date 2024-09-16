from django.core.management.base import BaseCommand
import pandas as pd
from central.models import School
class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        
        df = pd.read_csv('universities.csv')
        for NAME, ADDRESS in zip(df.Name,df.Address):
            models = School(name=NAME, address=ADDRESS)
            models.save()
