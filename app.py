from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch data from the API
    api_url = 'https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2024-07-09&end_date=2024-07-23&hourly=temperature_2m'
    response = requests.get(api_url)
    if response.status_code == 200:
        api_data = response.json()
    else:
        api_data = {}

    # Pass the data to the HTML template
    return render_template('index.html', data=api_data)

if __name__ == '__main__':
    app.run(debug=True)
