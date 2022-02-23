import os

current_price = 100

def get_database_connection():
    '''
        Creates a connection between selected database
    '''
    import sqlite3
    sqlite_file = 'smallcase.db'
    file_exists = os.path.isfile(sqlite_file)
    conn = sqlite3.connect(sqlite_file)
    if not file_exists:
        create_sqlite_tables(conn)
    return conn


def create_sqlite_tables(conn):
    '''
        Creates a sqlite table as specified in schema_sqlite.sql file
    '''
    cursor = conn.cursor()
    with open('schema_sqlite.sql', 'r') as schema_file:
        cursor.executescript(schema_file.read())
    conn.commit()


def insert_into_portfolio(ticker, total_shares, average_price):
    '''
        To insert ticker into portfolio
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO portfolio(ticker, shares, average_price) VALUES (?, ?, ?)", (ticker, total_shares, average_price))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_portfolio():
    '''
        To get all the tickers from portfolio
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT ticker, shares, average_price FROM portfolio where shares != 0')
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()

def get_ticker_from_portfolio(ticker):
    '''
        To get ticker from portfolio
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM portfolio where ticker=?', (ticker,))
        results = cursor.fetchone()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()

def update_portfolio(ticker, total_shares, average_price):
    '''
        To update the portfolio
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE portfolio SET shares=?, average_price=? WHERE ticker=?", (total_shares, average_price, ticker))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def add_new_transactions(ticker, shares, trade):
    '''
        To add a new transaction
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transactions(ticker, shares, trade) VALUES (?, ?, ?)", (ticker, shares, trade))
        conn.commit()
        cursor.close()
    except:
        cursor.close()

def get_transactions_for_ticker(ticker):
    '''
        To get transactions by tickername
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT ticker, shares, trade, created_at FROM transactions where ticker=? order by created_at desc', (ticker,))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()

def create_trade(trade, ticker, shares):
    '''
        To create a trade
    '''
    ticker_from_portfolio = get_ticker_from_portfolio(ticker)
    if(ticker_from_portfolio):

        previous_shares = ticker_from_portfolio[2]
        average_price = ticker_from_portfolio[3]

        if(trade == 'BUY'):
            total_shares = previous_shares + shares
            average_price = ((previous_shares * average_price) + (shares * current_price)) / total_shares
            update_portfolio(ticker, total_shares, average_price)
            add_new_transactions(ticker, shares, trade)
        else:

            if(previous_shares < shares):
                return False
            
            total_shares = previous_shares - shares
            update_portfolio(ticker, total_shares, average_price)
            add_new_transactions(ticker, shares, trade)
    else:
        average_price = shares * current_price / shares
        insert_into_portfolio(ticker, shares, average_price)
        add_new_transactions(ticker, shares, trade)

    return True

def get_cumulative_returns():
    '''
        To calculate the cumulative returns on the portfolio
    '''
    portfolio = get_portfolio()

    if(not portfolio):
        return -1

    cumulative_return = 0
    for item in portfolio:
        current_quantity = item[1]
        average_price = item[2]

        cumulative_return += (current_price - average_price) * current_quantity

    return cumulative_return