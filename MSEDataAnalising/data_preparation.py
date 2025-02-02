import pandas as pd


def load_and_clean_data(file_path):
    """
    Вчитува и обработува CSV фајлот.

    :param file_path: Патека до CSV фајлот.
    :return: Чистен Pandas DataFrame.
    """
    data = pd.read_csv(file_path)

    # Чистење и форматирање на податоците

    data['date'] = pd.to_datetime(data['date'], errors='coerce')



    data['last_transaction_price'] = data['last_transaction_price'].str.replace(',', '').str.replace('"', '').astype(
        float)

    # Пополнување на празните вредности, ако има
    data['max_price'] = data['max_price'].fillna(data['last_transaction_price'])
    data['min_price'] = data['min_price'].fillna(data['last_transaction_price'])
    data['avg_price'] = data['avg_price'].fillna(data['last_transaction_price'])

    return data
