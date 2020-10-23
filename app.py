from datetime import datetime

import yfinance as yf
from flask import Flask, request, render_template, Response
from yahoo_fin import stock_info as si


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def submit():
    if request.method == 'POST':
        if request.form.get("TopGainers"):
            top_gainers = si.get_day_gainers()
            file_name = "TopGainers-"+ str(datetime.today()).split()[0] + '.csv'
            return Response(
                top_gainers.to_csv(),
                mimetype="text/csv",
                headers={"Content-disposition":
                             f"attachment; filename={file_name}"})
        elif request.form.get("TopLosers"):
            top_losers = si.get_day_losers()
            file_name = "TopLosers-"+ str(datetime.today()).split()[0] + '.csv'
            return Response(
                top_losers.to_csv(),
                mimetype="text/csv",
                headers={"Content-disposition":
                             f"attachment; filename={file_name}"})

        elif request.form.get("MostActives"):
            most_active_stock = si.get_day_most_active()
            file_name = "MostActives-" + str(datetime.today()).split()[0] + '.csv'
            return Response(
                most_active_stock.to_csv(),
                mimetype="text/csv",
                headers={"Content-disposition":
                             f"attachment; filename={file_name}.csv"})


@app.route('/stock', methods=['POST'])
def stock():
    if request.method == 'POST':
        symbol = (request.form['symbol']).upper()
        start_date = datetime.strptime(request.form['start date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.form['end date'], '%Y-%m-%d').date()
        today = datetime.today().date()
        if (today < (start_date or end_date)) or (end_date < start_date):
            error = 'Your Date are not valid, try again'
            return render_template(
                'index.html',
                error=error)
        stock = yf.Ticker(symbol)
        data_download = yf.download(symbol, start=start_date, end=end_date)
        file_name = symbol + '.csv'
        return Response(
            data_download.to_csv(),
            mimetype="text/csv",
            headers={"Content-disposition":
                         f"attachment; filename={file_name}"})


if __name__ == '__main__':
    app.run(debug = True)
