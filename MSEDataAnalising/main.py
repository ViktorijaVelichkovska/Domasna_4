from data_preparation import load_and_clean_data

# Патека до обединетиот CSV фајл
file_path = "../../../MSEDataAnalising/servisi/LSTM/lstmmm/combined_data.csv"

# Вчитување и чистење на податоците
data = load_and_clean_data(file_path)

# Проверка на податоците
print(data.head())
