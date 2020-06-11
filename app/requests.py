from app import app
import urllib.request,json
from .models import Quote

quote_url = app.config['RANDOM_QUOTES_URL']

def get_quotes():
    '''
    Function that gets the json response to our url request
    '''
    with urllib.request.urlopen(quote_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quote_results = {}

        if get_quotes_response['id', 'author', 'quote']:
            quote_results['id'] = get_quotes_response['id']
            quote_results['author'] = get_quotes_response['author']
            quote_results['quote'] = get_quotes_response['quote']
    
    return quote_results