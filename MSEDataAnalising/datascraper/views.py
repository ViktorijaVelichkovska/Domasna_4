from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DayEntryAsString, Company
from .serializers import DayEntryAsStringSerializer, CompanySerializer
import logging
import csv
from rest_framework.views import APIView


logger = logging.getLogger(__name__)

# Функција за рендерирање на почетната страница
def home(request):
    return render(request, 'home.html')

# API за претворање на CSV во JSON
class CSVtoJSONAPIView(APIView):
    def get(self, request):
        csv_file_path = "indicators_with_signals.csv"
        data = []

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Поправка на децимали
                    for key, value in row.items():
                        if isinstance(value, str) and "," in value:
                            row[key] = value.replace(",", ".")

                    # Поправка на празни вредности
                    for key, value in row.items():
                        if value == "":
                            row[key] = None

                    # Поправка на формат на датум
                    if row["date"]:
                        row["date"] = datetime.strptime(row["date"], "%m/%d/%Y").strftime("%Y-%m-%d")

                    data.append(row)
                    print(f"Parsed row: {row}")  # Логирање

        except FileNotFoundError:
            return JsonResponse({"error": "CSV file not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        return JsonResponse(data, safe=False)

# Функција која враќа порака
def my_function(request):
    if request.method == 'GET':
        return JsonResponse({'message': 'Function called successfully!'})

# API за добивање на податоци со филтрирање по датум и компанија
@api_view(['GET'])
def get_data(request):
    company_code = request.query_params.get('company_code')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    try:
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    except ValueError:
        return Response({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=400)

    filters = {}
    if company_code:
        filters['company_code'] = company_code
    if start_date and end_date:
        filters['date__range'] = [start_date, end_date]

    data = DayEntryAsString.objects.filter(**filters)
    serializer = DayEntryAsStringSerializer(data, many=True)
    return Response(serializer.data)

# API за добивање на сите company_code вредности
@api_view(['GET'])
def get_company_codes(request):
    company_codes = Company.objects.all()
    serializer = CompanySerializer(company_codes, many=True)
    return Response(serializer.data)

# API за добивање на најновиот запис за дадени компании
@api_view(['GET'])
def get_last_day_data(request):
    company_codes = request.query_params.get('company_codes')

    if not company_codes:
        return Response({"error": "company_codes query parameter is required."}, status=400)

    company_codes = company_codes.split(',')
    data = []

    for code in company_codes:
        try:
            last_entry = DayEntryAsString.objects.filter(company_code=code).last()
            if last_entry:
                data.append(last_entry)
        except Exception as e:
            logger.error(f"Error fetching data for company code {code}: {e}")
            return Response({"error": f"Error fetching data for company code {code}"}, status=500)

    if not data:
        return Response({"error": "No data found for the given company codes."}, status=404)

    serializer = DayEntryAsStringSerializer(data, many=True)
    return Response(serializer.data)
