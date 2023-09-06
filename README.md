# Currency Exchange Rates to Google Sheets

This project fetches currency exchange rates and stores them in Google Sheets. The project consists of backend logic written in Python, and a frontend developed using HTML.

## Test version
- https://magnum2326.pythonanywhere.com
  
## Files

### Backend

- g.py
This file contains utility functions for connecting to Google's API services. It features the Create_Service function for creating Google API services and a convert_to_RFC_datetime function for date conversion.

- currency_sheets.py
This is the main Python file where the Flask app is defined. It uses the Google Sheets API to write fetched currency exchange rates into a Google Sheet. It has multiple routes including:

- /: Serves the main form page for date range input
- /fetch_rates: Fetches exchange rates for the given date range

### Frontend

- index.html
This is the main HTML file served by the Flask app. It contains a form where users can input a date range for which they want to fetch the exchange rate.

- success.html
This HTML file is displayed when the data is successfully fetched and stored in Google Sheets. It provides a button to go back to the main page.

### Usage

1. Clone the repository.

2. Navigate to the project folder and install dependencies:

```
pip install -r requirements.txt
```

3. Run the Flask app:

```
python currency_sheets.py
```

4. Open a web browser and go to http://127.0.0.1:5000/.

5. Enter a date range and click "Fetch Rates".

6. You will be redirected to a success page once the data is stored in Google Sheets.

### Dependencies
Flask
Google Sheets API
Requests

