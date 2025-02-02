from django.urls import path
from .views import *

urlpatterns = [
    path('api/get-company-predictions/', get_company_predictions, name='company-predictions'),
    path('api/get-prediction-for-company/', get_predictions_for_company, name='prediction-for-company'),
    path('api/get-latest-newss/', get_latest_newss, name='lates-newss'),
]