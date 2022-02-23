from flask import (
    Flask, request
)
from flask_restplus import Api, Resource, fields

from modules import functions

app = Flask(__name__)

api_app = Api(app = app)

name_space = api_app.namespace('', description='Main APIs')

@name_space.route("/")
class Class(Resource):
	def get(self):
		return {
			"status": "Got new data"
		}
	def post(self):
		return {
			"status": "Posted new data"
		}

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

@app.route('/')
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