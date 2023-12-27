# Get the code to send sms using twilio - https://www.twilio.com/docs/messaging/quickstart/python
# Get the news api - https://newsapi.org/docs/endpoints/everything
# Get the auth_token and account_sid - https://console.twilio.com/

import os
import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

ACC_SID = os.environ.get("ACCOUNT_SID")
AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.environ.get("STOCK_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
    "apikey": STOCK_API_KEY
}
response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
# print(response.json())


# Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries.
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_closing_price = float(data_list[0]['4. close'])

# Get the day before yesterday's closing stock price
day_before_yesterday_closing_price = float(data_list[1]['4. close'])
# print(day_before_yesterday_closing_price)

difference = abs(yesterday_closing_price - day_before_yesterday_closing_price)
# print(difference)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"
percentage_difference = (difference / float(yesterday_closing_price)) * 100
# print(percentage_difference)

if abs(percentage_difference) > 0:  # CHANGE 0 VALUE TO THE VALUE U WANT
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news = requests.get(NEWS_ENDPOINT, news_params)
    news.raise_for_status()
    articles = news.json()['articles']
    three_articles = articles[:3]

formatted_articles = [
    f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for
    article in three_articles]
print(formatted_articles)

client = Client(ACC_SID, AUTH_TOKEN)

for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_=os.environ.get("SEND_FROM_MOBILE_NUMBER"),
        to=os.environ.get("SEND_TO_MOBILE_NUMBER")
    )

# print(message.sid)



