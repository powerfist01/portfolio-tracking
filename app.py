from flask import (
    Flask, request
)

from modules import functions

app = Flask(__name__)

@app.route('/')
def home():

  return '<b>server is running!</b><br><br>Documentation: <br> 1. <b>GET /</b> Home page <br>2.<b> GET /portfolio</b> Get my portfolio <br>3. <b>POST /trade </b>To perform a trade <br>4. <b>GET /transactions </b>To get all the transactions in the portfolio <br> 5.<b> GET/returns </b>To get the cumulative returns'

@app.route('/trade', methods=['POST'])
def trade():

  if request.method == 'POST':
    trade = request.form['trade']
    ticker = request.form['ticker']
    shares = int(request.form['shares'])
    
    trade_event = functions.create_trade(trade, ticker, shares)

    if(trade_event):
      return {'success': True, 'message': 'Trade successfull'}
    else:
      return {'success': False, 'message': 'Total shares cannot be negative.'}

@app.route('/portfolio')
def portfolio():

  my_portfolio = functions.get_portfolio()
  return my_portfolio

@app.route('/transactions', methods=['POST'])
def history():

  if request.method == 'POST':
    ticker = request.form['ticker']
    transactions = functions.get_transactions_for_ticker(ticker)
    if(transactions):
      return {'success': True, 'transactions': transactions}
    else:
      return {'success': False}
  
@app.route('/returns')
def returns():
  
  returns = functions.get_cumulative_returns()
  if(returns >= 0):
    return {'success': True, 'cumulative returns': returns}
  else:
    return {'success': False}

if __name__ == '__main__':
  app.run(debug=True)