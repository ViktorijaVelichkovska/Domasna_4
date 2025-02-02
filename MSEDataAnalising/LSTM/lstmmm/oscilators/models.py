from django.db import models
# Create your models here.

# python manage.py makemigrations - on every change
# python manage.py migrate

class DayEntry(models.Model):
    date = models.DateField(null=True, blank=True)
    last_transaction_price = models.FloatField(null=True, blank=True)
    max_price = models.FloatField(null=True, blank=True)
    min_price = models.FloatField(null=True, blank=True)
    avg_price = models.FloatField(null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    profit = models.FloatField(null=True, blank=True)
    total_profit = models.FloatField(null=True, blank=True)
    company_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.date} - {self.company_code}"

    class Meta:
        ordering = ['date']
        app_label = 'datascraper'
        unique_together = ('company_code', 'date')

class DayEntryAsString(models.Model):
    date = models.DateField(null=True, blank=True)
    date_string = models.CharField(max_length=50, null=True, blank=True)
    last_transaction_price = models.CharField(max_length=50, null=True, blank=True)
    max_price = models.CharField(max_length=50, null=True, blank=True)
    min_price = models.CharField(max_length=50, null=True, blank=True)
    avg_price = models.CharField(max_length=50, null=True, blank=True)
    percentage = models.CharField(max_length=50, null=True, blank=True)
    profit = models.CharField(max_length=50, null=True, blank=True)
    total_profit = models.CharField(max_length=50, null=True, blank=True)
    company_code = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.date} - {self.company_code}"

    class Meta:
        ordering = ['date']
        app_label = 'datascraper'
        unique_together = ('company_code', 'date')


class Company(models.Model):
    name = models.CharField(null=False, max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

from django.db import models

class CompanyTransaction(models.Model):
    date = models.DateField()  # Датум на трансакцијата
    last_transaction_price = models.CharField(max_length=20, blank=True, null=True)  # Цена на последна трансакција
    max_price = models.CharField(max_length=20, blank=True, null=True)  # Максимална цена
    min_price = models.CharField(max_length=20, blank=True, null=True)  # Минимална цена
    avg_price = models.CharField(max_length=20, blank=True, null=True)  # Просечна цена
    percentage = models.CharField(max_length=20, blank=True, null=True)  # Процентуална промена
    profit = models.DecimalField(max_digits=15, decimal_places=2)  # Добивка
    total_profit = models.CharField(max_length=50)  # Вкупна добивка
    company_code = models.CharField(max_length=10)  # Код на компанијата

    def __str__(self):
        return f"{self.company_code} on {self.date}"
# NLP/models.py

from django.db import models

class News(models.Model):
    document_id = models.CharField(max_length=255, unique=True)
    date = models.DateField()
    description = models.TextField()
    content = models.TextField()
    company_code = models.CharField(max_length=50)
    company_name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title
