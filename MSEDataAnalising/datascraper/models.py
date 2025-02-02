from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']



class BaseDayEntry(models.Model):
    date = models.DateField(null=True, blank=True)
    company_code = models.CharField(max_length=50)

    class Meta:
        abstract = True
        ordering = ['date']
        app_label = 'datascraper'
        unique_together = ('company_code', 'date')



class DayEntry(BaseDayEntry):
    last_transaction_price = models.FloatField(null=True, blank=True)
    max_price = models.FloatField(null=True, blank=True)
    min_price = models.FloatField(null=True, blank=True)
    avg_price = models.FloatField(null=True, blank=True)
    percentage = models.FloatField(null=True, blank=True)
    profit = models.FloatField(null=True, blank=True)
    total_profit = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.company_code}"



class DayEntryAsString(BaseDayEntry):
    date_string = models.CharField(max_length=50, null=True, blank=True)
    last_transaction_price = models.CharField(max_length=50, null=True, blank=True)
    max_price = models.CharField(max_length=50, null=True, blank=True)
    min_price = models.CharField(max_length=50, null=True, blank=True)
    avg_price = models.CharField(max_length=50, null=True, blank=True)
    percentage = models.CharField(max_length=50, null=True, blank=True)
    profit = models.CharField(max_length=50, null=True, blank=True)
    total_profit = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.date} - {self.company_code}"


    def convert_to_day_entry(self):
        return DayEntry(
            date=self.date,
            last_transaction_price=self._convert_to_float(self.last_transaction_price),
            max_price=self._convert_to_float(self.max_price),
            min_price=self._convert_to_float(self.min_price),
            avg_price=self._convert_to_float(self.avg_price),
            percentage=self._convert_to_float(self.percentage),
            profit=self._convert_to_float(self.profit),
            total_profit=self._convert_to_float(self.total_profit),
            company_code=self.company_code
        )


    def _convert_to_float(self, value):
        try:
            return float(value) if value else None
        except ValueError:
            return None
