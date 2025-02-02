from .models import News, Company


def get_all_predictions():
    data = Company.objects.all()
    return data


def get_prediciton_for(code):
    data = Company.objects.filter(company_code=code)
    return data


def get_last_newss(number):
    data = News.objects.all()[::-1][:number]
    return data