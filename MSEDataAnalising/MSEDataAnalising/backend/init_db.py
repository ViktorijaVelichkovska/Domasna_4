import pandas as pd
import sqlite3

# Патека до CSV фајлот
csv_file_path = '../../datascraper/indicators_with_signals.csv'

# Поврзување со SQLite база (ќе се креира ако не постои)
conn = sqlite3.connect('../data.db')

# Вчитување на CSV податоци
data = pd.read_csv(csv_file_path)

# Запишување на податоците во табела наречена 'indicators'
data.to_sql('indicators', conn, if_exists='replace', index=False)

print("Податоците се успешно зачувани во базата!")
conn.close()
