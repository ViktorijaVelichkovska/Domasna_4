from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('datascraper.urls')),
    path('lstmmm/', include('LSTM.urls')),
    path('nlp/', include('NLP.urls')),



]

