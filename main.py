import logging
import requests
import matplotlib.pyplot as plt
import base64

from io import BytesIO
#from googleapiclient.discovery import build
#from oauth2client.service_account import ServiceAccountCredentials
from flask import Flask, render_template, request
from pytrends.request import TrendReq
app = Flask(__name__)



@app.route('/', methods=["GET","POST"])
def home():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-251038264-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-251038264-1');
    </script>
    """

    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            pass # do something
        else:
            pass # unknown
    elif request.method == 'GET':
        return prefix_google + render_template('home.html')

    return prefix_google + render_template("home.html")

@app.route('/cookies')
def cookies():
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a251038264w345003629p281149860")
    return req.text

@app.route('/logger')
def printLogs():
    app.logger.warning('testing warning log')
    app.logger.error('testing error log')
    app.logger.info('testing info log')
    return render_template('logs.html')


from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

@app.route('/trend')
def trend_plot():
    # Get the trend data using pytrends
    pytrends = TrendReq()
    kw_list = ['geneve']
    pytrends.build_payload(kw_list=kw_list, timeframe='today 5-y')
    trend_data = pytrends.interest_over_time()

    # Create a line chart using Matplotlib
    plt.plot(trend_data['geneve'])
    plt.xlabel('Date')
    plt.ylabel('Trend')

    # Save the chart to a PNG file
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode the chart in base64
    chart_url = base64.b64encode(buf.getvalue()).decode()
    plt.clf()

    # Render the chart in an HTML template
    return render_template('trend_plot.html', chart_url=chart_url)