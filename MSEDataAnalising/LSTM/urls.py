from django.urls import path
from .views import lstm_predictions, oscillator_signals, moving_average_signals, time_series_analysis

urlpatterns = [
    path('api/lstm-predictions/', lstm_predictions, name='lstm-predictions'),
    path('api/oscillator-signals/', oscillator_signals, name='oscillator-signals'),
    path('api/moving-average-signals/', moving_average_signals, name='moving-average-signals'),
    path('api/time-series-analysis/', time_series_analysis, name='time-series-analysis')
]

