from django.db import models


class News(models.Model):
    document_id = models.IntegerField(unique=True, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    company_code = models.CharField(max_length=20, null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)
    sentiment = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.document_id} - {self.date} - {self.sentiment}"

    class Meta:
        ordering = ['date']

class Company(models.Model):
    company_code = models.CharField(null=False, max_length=50, unique=True)
    company_name = models.CharField(null=False, max_length=50, default="")
    max_sentiment = models.CharField(max_length=10, default='neutral')
    max_sentiment_value = models.FloatField(default=0.5)

    def __str__(self):
        return f"{self.company_code} - {self.max_sentiment} - {self.max_sentiment_value}"

    class Meta:
        ordering = ['company_code']
