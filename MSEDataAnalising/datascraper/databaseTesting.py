import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()

from datascraper.models import DayEntry, DayEntryAsString


def get_last_date(company_code):
    last_entry = DayEntry.objects.filter(company_code=company_code).order_by('-date').first()
    if last_entry:
        return company_code, last_entry.date
    return company_code, None


def get_last_date_string(company_code):
    last_entry = DayEntryAsString.objects.filter(company_code=company_code).order_by('-date').first()
    if last_entry:
        return company_code, last_entry.date
    return company_code, None



company_code = "ADIN"
company_code, last_date = get_last_date_string(company_code)

if last_date:
    print(f"Poslednji datum za {company_code}: {last_date}")
else:
    print(f"Nema podataka za {company_code}")
