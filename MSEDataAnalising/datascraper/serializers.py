from rest_framework import serializers
from .models import DayEntryAsString, Company


class DayEntryAsStringSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayEntryAsString
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['name']


class TimeSeriesDataSerializer(serializers.ModelSerializer):
    date = serializers.DateField()
    total_profit = serializers.FloatField()

    class Meta:
        model = DayEntryAsString
        fields = ['date', 'total_profit']

    def to_representation(self, instance):

        representation = super().to_representation(instance)


        processed_total_profit = self._process_total_profit(instance.total_profit)


        representation['total_profit'] = processed_total_profit

        return representation

    def _process_total_profit(self, total_profit):
        """Helper method to process total_profit into a float."""
        raw_value = str(total_profit).replace(',', '.')

        try:
            return float(raw_value)
        except ValueError:
            return None
