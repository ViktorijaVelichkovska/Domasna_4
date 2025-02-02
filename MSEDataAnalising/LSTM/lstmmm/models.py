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