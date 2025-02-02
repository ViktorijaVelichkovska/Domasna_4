import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MSEDataAnalising.settings')
django.setup()
from datascraper.models import DayEntryAsString, Company

# Create your tests here.

companies = Company.objects.all()
print(len(companies))
for c in companies:
    c_d = DayEntryAsString.objects.filter(company_code=c.name)
    print(c.name + " - " + str(len(c_d)))
    if c.name == "ALK":
        for cd in c_d:
            print(cd)