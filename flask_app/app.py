from flask import Flask, render_template, request, redirect, url_for
import webbrowser
import json
import urllib.parse
import re

app = Flask(__name__)

def extract_first_word(text):
    # Split the text into words and return the first word
    words = text.strip().split()
    return words[0] if words else ""


state_abbreviations = {
    'ALABAMA': 'AL',
    'ALASKA': 'AK',
    'ARIZONA': 'AZ',
    'ARKANSAS': 'AR',
    'CALIFORNIA': 'CA',
    'COLORADO': 'CO',
    'CONNECTICUT': 'CT',
    'DELAWARE': 'DE',
    'FLORIDA': 'FL',
    'GEORGIA': 'GA',
    'HAWAII': 'HI',
    'IDAHO': 'ID',
    'ILLINOIS': 'IL',
    'INDIANA': 'IN',
    'IOWA': 'IA',
    'KANSAS': 'KS',
    'KENTUCKY': 'KY',
    'LOUISIANA': 'LA',
    'MAINE': 'ME',
    'MARYLAND': 'MD',
    'MASSACHUSETTS': 'MA',
    'MICHIGAN': 'MI',
    'MINNESOTA': 'MN',
    'MISSISSIPPI': 'MS',
    'MISSOURI': 'MO',
    'MONTANA': 'MT',
    'NEBRASKA': 'NE',
    'NEVADA': 'NV',
    'NEW HAMPSHIRE': 'NH',
    'NEW JERSEY': 'NJ',
    'NEW MEXICO': 'NM',
    'NEW YORK': 'NY',
    'NORTH CAROLINA': 'NC',
    'NORTH DAKOTA': 'ND',
    'OHIO': 'OH',
    'OKLAHOMA': 'OK',
    'OREGON': 'OR',
    'PENNSYLVANIA': 'PA',
    'RHODE ISLAND': 'RI',
    'SOUTH CAROLINA': 'SC',
    'SOUTH DAKOTA': 'SD',
    'TENNESSEE': 'TN',
    'TEXAS': 'TX',
    'UTAH': 'UT',
    'VERMONT': 'VT',
    'VIRGINIA': 'VA',
    'WASHINGTON': 'WA',
    'WEST VIRGINIA': 'WV',
    'WISCONSIN': 'WI',
    'WYOMING': 'WY',
}

def extract_value(text, field):
    pattern = rf"{field}:\s*(.*?)\s*(?=\n|$)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else ""

def construct_zillow_url(area, max_price, min_size, min_bedrooms, min_bathrooms, basement):
    base_url = f"https://www.zillow.com/{area}/houses/"
    
    filter_state = {
        "price": {
            "min": 0,
            "max": int(max_price) if max_price.isdigit() else None
        },
        "sqft": {
            "min": int(min_size) if min_size.isdigit() else None
        },
        "beds": {
            "min": int(min_bedrooms) if min_bedrooms.isdigit() else None
        },
        "baths": {
            "min": int(min_bathrooms) if min_bathrooms.isdigit() else None
        }
    }
    
    search_query_state = {
        "pagination": {},
        "isMapVisible": True,
        "usersSearchTerm": area,
        "filterState": filter_state,
        "isListVisible": True,
        "mapZoom": 15
    }

    encoded_query = urllib.parse.quote(json.dumps(search_query_state))
    url = f"{base_url}?searchQueryState={encoded_query}"
    
    return url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['user_input']

        state_name = extract_first_word(user_input)
        city = extract_value(user_input, "City")
        max_price = extract_value(user_input, "Max Price").replace('$', '').replace(',', '')
        min_size = extract_value(user_input, "Sqft Min").replace(' sqft', '')
        min_bedrooms = extract_value(user_input, "Bed Min")
        min_bathrooms = extract_value(user_input, "Bath Min")
        basement = extract_value(user_input, "Basement")
        
        state_abbreviation = state_abbreviations.get(state_name.upper(), 'Unknown')
        
        area = f"{city}-{state_abbreviation}"
        url = construct_zillow_url(area, max_price, min_size, min_bedrooms, min_bathrooms, basement)

        # Open the URL in a new tab
        webbrowser.open(url)
        
        return redirect(url_for('index'))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
