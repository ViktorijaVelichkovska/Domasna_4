from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .services import *


@api_view(['GET'])
def get_company_predictions(request):
    data = get_all_predictions()
    serializer = CompanySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_predictions_for_company(request):
    company_code = request.query_params.get('company_code')
    data = get_prediciton_for(company_code)
    serializer = CompanySerializer(data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_latest_newss(request):
    number_of_news = request.query_params.get('number_of_news')
    try:
        number_of_news = int(number_of_news)
    except ValueError:
        number_of_news = 3
    data = get_last_newss(number_of_news)
    serializer = NewsSerializer(data, many=True)
    return Response(serializer.data)