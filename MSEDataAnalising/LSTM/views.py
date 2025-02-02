from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views_utils import (get_lstm_predictions, get_oscillator_signals, get_moving_average_signals,
                         perform_time_series_analysis)

# views.py
from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')  # или што и да сакаш да прикажеш

@api_view(['GET'])
def lstm_predictions(request):
    company_code = request.query_params.get('company_code')
    try:
        response_data = get_lstm_predictions(company_code)
        return Response(response_data)
    except ValueError as e:
        return Response({"error": str(e)})
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)})


@api_view(['GET'])
def oscillator_signals(request):
    company_code = request.query_params.get('company_code')
    try:
        response_data = get_oscillator_signals(company_code)
        return Response(response_data)
    except ValueError as e:
        return Response({"error": str(e)})
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)})


@api_view(['GET'])
def moving_average_signals(request):
    company_code = request.query_params.get('company_code')
    try:
        response_data = get_moving_average_signals(company_code)
        return Response(response_data)
    except ValueError as e:
        return Response({"error": str(e)})
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)})


@api_view(['GET'])
def time_series_analysis(request):
    company_code = request.query_params.get('company_code')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    try:
        response_data = perform_time_series_analysis(company_code, start_date, end_date)
        return Response(response_data)
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    except Exception as e:
        return Response({"error": "An unexpected error occurred: " + str(e)}, status=500)