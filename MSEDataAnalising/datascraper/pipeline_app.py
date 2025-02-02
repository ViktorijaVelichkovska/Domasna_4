from flask import Flask, render_template, request, redirect, url_for
import subprocess

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('datascraper.html')

@app.route('/run_pipeline', methods=['POST'])
def run_pipeline():
    try:
        result = subprocess.run(['python', 'datascraper/pipeline.py'], check=True, capture_output=True, text=True)
        output = result.stdout
        return render_template('datascraper.html', output=output)
    except subprocess.CalledProcessError as e:
        error_output = e.stderr
        return f"An error occurred: {e}\nError Output: {error_output}"


if __name__ == '__main__':
    app.run(debug=True)