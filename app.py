# Yuxin Zhou   CMPE285   HW2
from flask import Flask, render_template, request
import time
from time import ctime
from time import time as ti
import yfinance as yf
from datetime import datetime
import pytz
from pytz import timezone
import urllib.request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    time_info = None
    name_info = None
    prince_info = None
    
    if request.method == 'POST':
        if request.form['symbol']:
                if connect_internet():
                    symbol = request.form['symbol']
                    info = get_stock_info(symbol)
                    if info:
                        time_info = get_time_info()
                        name_info = info[0]
                        prince_info = info[1]
                    else:
                        error = "Input stock symbol does not exisit. Please try again!"
                else:
                    error = "No internet connection. Please connect to the internet!"
        else:
            error = "Empty input. Please try again!"
    return render_template('index.html', error=error, time_info=time_info, name_info = name_info, prince_info = prince_info)


def get_time_info():
    timezone = pytz.timezone('US/Pacific')
    utc_time = datetime.utcnow()
    time_in_seconds = int(pytz.utc.localize(utc_time, is_dst=None).astimezone(timezone).strftime('%s'))
    current_time = ctime(time_in_seconds)
    current_time_info = current_time.rsplit(" ", 1)[0]
    year = current_time.rsplit(" ", 1)[1]
    time_zone_abbr = datetime.now(timezone).strftime("%Z")
    time_print_out = current_time_info + " " + time_zone_abbr + " " + year
    return time_print_out

def get_stock_info(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    todays_data = ticker.history(period='1d')
    if info:
        if 'longName' in info:
            name = info['longName'] + " (" + symbol.upper() + ")"
            current_price = round(todays_data['Close'][0], 2)
            prev_close = info['previousClose']
            value_change = current_price - prev_close
            percentage_change = (value_change / prev_close)*100
            value_change = round(value_change, 2)
            percentage_change = round(percentage_change, 2)
            value_change_str = str(value_change)
            percentage_change_str = str(percentage_change)
            if (value_change > 0):
                value_change_str = "+" + str(value_change)
            if (percentage_change > 0):
                percentage_change_str = "+" + str(percentage_change)
            price_output = str(current_price) + " " + value_change_str + " (" + percentage_change_str + "%)"
            return [name, price_output]
        else:
            None
    else:
        return None



def connect_internet():
    try:
        urllib.request.urlopen('http://google.com') 
        return True
    except:
        return False
