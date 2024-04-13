from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    data = request.get_json()
    source_curr = data['queryResult']['parameters']['unit-currency']['currency']
    amount = data['queryResult']['parameters']['unit-currency']['amount']
    target_currency = data['queryResult']['parameters']['currency-name']
    print(source_curr)
    print(amount)
    print(target_currency)
    conversion_rate = fetch_currency(source_curr, target_currency)
    finalamount=amount * conversion_rate
    print(finalamount)
    finalamount=round(finalamount,2)

    response_text={
        'fulfillmentText':"{} {} is {} {}".format(amount,source_curr,finalamount,target_currency)
    }
    return jsonify(response_text)

def fetch_currency(source, target):
    url = f"https://api.freecurrencyapi.com/v1/latest?apikey=fca_live_AAt8fyeVKvdEzuoe2XvkAwsxQcV4ANumnRVCebrb&source={source}&target={target}"
    response = requests.get(url)
    data = response.json()
    if 'data' in data and target in data['data']:
        return data['data'][target]
    else:
        return "Conversion rate not available"

if __name__ == '__main__':
    app.run(debug=True)


