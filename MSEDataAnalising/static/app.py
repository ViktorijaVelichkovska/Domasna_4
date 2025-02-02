"""from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/get_data', methods=['GET'])
def get_data():
    # Прочитај го CSV фајлот во pandas DataFrame
    df = pd.read_csv('indicators_with_signals.csv.csv')

    # Конвертирај ги податоците од DataFrame во речник (кој може да се конвертира во JSON)
    data = df.to_dict(orient='records')

    # Испрати ги податоците како JSON
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
"""