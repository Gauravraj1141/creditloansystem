# injest_customer_data.py
from django.core.management.base import BaseCommand
from creditloan.views import run_background_workers

class Command(BaseCommand):
    help = 'Injest customer data'

    def handle(self, *args, **kwargs):
        run_background_workers()
