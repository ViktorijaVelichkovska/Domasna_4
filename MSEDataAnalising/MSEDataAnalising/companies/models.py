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
