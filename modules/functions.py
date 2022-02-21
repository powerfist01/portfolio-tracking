import os
import hashlib


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


def get_user_count():
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users')
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False


def check_user_exists(username, password):
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        result = cursor.fetchone()
        if result:
            return result[0]
    except:
        return False


def store_last_login(user_id):
    '''
        Checks whether a user exists with the specified username and password
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_login=(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id=?", (user_id, ))
        conn.commit()
        cursor.close()
    except:
        cursor.close()


def check_username(username):
    '''
        Checks whether a username is already taken or not
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username, ))
        if cursor.fetchone():
            return True
    except:
        return False


def signup_user(username, password, email):
    '''
        Function for storing the details of a user into the database
        while registering
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users(username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def get_user_data(user_id):
    '''
        Function for getting the data of a specific user using his user_id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id=?', (str(user_id), ))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()


def get_data_using_user_id(id):
    '''
        Function for getting the data of all notes using user_id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        if len(results) == 0:
            return None
        return results
    except:
        cursor.close()


def get_data_using_id(id):
    '''
        Function for retrieving data of a specific note using its id
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes WHERE id=' + str(id))
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()


def get_number_of_notes(id):
    '''
        Function for retrieving number of notes stored by a specific user
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(note) FROM notes WHERE user_id=' + str(id))
        results = cursor.fetchone()[0]
        cursor.close()
        return results
    except:
        cursor.close()


def get_data():
    '''
        Function for getting data of all notes
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM notes')
        results = cursor.fetchall()
        cursor.close()
        return results
    except:
        cursor.close()


def add_note(note_title, note, note_markdown, tags, user_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO notes(note_title, note, note_markdown, tags, user_id) VALUES (?, ?, ?, ?, ?)", (note_title, note, note_markdown, tags, user_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()


def edit_note(note_title, note, note_markdown, tags, note_id):
    '''
        Function for adding note into the database
    '''
    conn = get_database_connection()
    try:
        cursor = conn.cursor()
        # print("UPDATE notes SET note_title=?, note=?, note_markdown=?, tags=? WHERE id=?", (note_title, note, note_markdown, tags, note_id))
        cursor.execute("UPDATE notes SET note_title=?, note=?, note_markdown=?, tags=? WHERE id=?", (note_title, note, note_markdown, tags, note_id))
        conn.commit()
        cursor.close()
        return
    except:
        cursor.close()
