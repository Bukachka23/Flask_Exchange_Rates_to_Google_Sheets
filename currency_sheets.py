import logging
logging.basicConfig(level=logging.DEBUG)

from flask import Flask, jsonify, request, render_template
import requests
from datetime import datetime, timedelta
from g import Create_Service

# Initialize Google Sheets API
CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)

# Define the ID of the Google Sheet you want to write to
SPREADSHEET_ID = '14JhkwvT5sICJo5bZdV6_idmRiyInLqaCpHJGRrO28so'
SHEET_NAME = 'Sheet1'

app = Flask(__name__)


# Function to fetch the exchange rate for a specific date from Privatbank API
def fetch_exchange_rate(date):
    # Construct the URL with the date parameter
    url = f"https://api.privatbank.ua/p24api/exchange_rates?date={date}"
    # Make an HTTP GET request
    response = requests.get(url)
    # Raise an exception if the request was not successful
    response.raise_for_status()
    # Parse the JSON response
    raw_data = response.json()
    # Extract the 'exchangeRate' field or default to an empty list
    exchange_rates = raw_data.get("exchangeRate", [])

    # Loop through each item in the exchange rates
    for item in exchange_rates:
        # Check if the currency is USD
        if item.get('currency', '') == 'USD':
            # Return the relevant data as a dictionary
            return {
                'Base Currency': item.get('baseCurrency', 'N/A'),
                'Target Currency': item.get('currency', 'N/A'),
                'Sale Rate': item.get('saleRate', 'N/A'),
                'Purchase Rate': item.get('purchaseRate', 'N/A'),
                'Sale Rate NB': item.get('saleRateNB', 'N/A'),
                'Purchase Rate NB': item.get('purchaseRateNB', 'N/A')
            }
    # Return None if USD data is not found
    return None


# Function to write the fetched data to Google Sheets
def write_to_gsheets(data):
    # Prepare the data for Google Sheets in the required format
    values = [[
        data['Date'],
        data['Exchange Rate']['Base Currency'],
        data['Exchange Rate']['Target Currency'],
        data['Exchange Rate']['Sale Rate'],
        data['Exchange Rate']['Purchase Rate'],
        data['Exchange Rate']['Sale Rate NB'],
        data['Exchange Rate']['Purchase Rate NB']
    ]]
    # Construct the body payload for Google Sheets
    body = {'values': values}

    # Define the range where the data will be written in Google Sheets
    range_name = f"{SHEET_NAME}!A:G"
    # Use Google Sheets API to append the data
    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        body=body,
        valueInputOption="USER_ENTERED"
    ).execute()


# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for fetching exchange rates from Privatbank API
@app.route('/fetch_rates')
def get_privatbank_exchange_rates():
    try:
        # Get the start and end date parameters from the URL, default to today's date
        start_date_param = request.args.get('start_date', datetime.now().strftime('%d.%m.%Y'))
        end_date_param = request.args.get('end_date', datetime.now().strftime('%d.%m.%Y'))

        # Convert the date parameters to datetime objects
        start_date = datetime.strptime(start_date_param, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_param, '%Y-%m-%d')

        # Calculate the number of days between the start and end dates
        delta = end_date - start_date

        # Initialize a list to store all the results
        all_results = []

        # Loop through each day in the date range
        for i in range(delta.days + 1):
            # Format the date
            date = (start_date + timedelta(days=i)).strftime('%d.%m.%Y')
            # Fetch the exchange rate for the date
            exchange_rate = fetch_exchange_rate(date)
            # Check if exchange rate exists
            if exchange_rate:
                # Prepare the data
                data = {'Date': date, 'Exchange Rate': exchange_rate}
                # Append the data to the results list
                all_results.append(data)
                # Write the data to Google Sheets
                write_to_gsheets(data)

        # Return a success page instead of JSON data
        return render_template('success.html')

    except requests.RequestException as e:
        # Handle any exceptions that occur during the HTTP request
        return jsonify({'error': f'Failed to make HTTP request: {e}'}), 400



if __name__ == '__main__':
    app.run(debug=True)
