from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('csv-to-json/', views.CSVtoJSONAPIView.as_view(), name='csv_to_json'),
    path('api/get-data/', views.get_data, name='get_data'),  # Префикс за api
    path('get-company-codes/', views.get_company_codes, name='get_company_codes'),
    path('get-last-day-data/', views.get_last_day_data, name='get_last_day_data'),
    path('my-function/', views.my_function, name='my_function')
]
