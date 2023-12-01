from flask import Flask, render_template, request
import sqlite3, os, re

app = Flask(__name__)

def initDB():
    db_file = 'example.db'
    if not os.path.exists(db_file):
        os.system('touch '+db_file)
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, pass TEXT, flag TEXT)')
    cursor.execute('SELECT * FROM users WHERE username = \'admin\'')
    existing_admin = cursor.fetchone()
    if not existing_admin:
        cursor.execute('INSERT INTO users (username, pass, flag) VALUES (\'admin\', \'w34kP455\', \'dhWGkGJF$Nvkau!MebVdcDQGxrCzfbuH8DFpfTxV&46x&LD5&^ZT3nZ\')')
    conn.commit()
    conn.close()

def validateLogin(input):
    whitelist_pattern = r'^[0-9a-zA-Z_\-!@$£]+$'
    pattern = re.compile(whitelist_pattern)
    return bool(pattern.match(input))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if not validateLogin(username) or not validateLogin(password):
        return render_template('index.html', results='Sorry this user input is invalid!\nWe only accept a-z,A-Z,0-9,_-!@$£')
    #query = f\"SELECT * FROM users WHERE username = '{username}' AND pass = '{password}'\"
    query=f"SELECT * FROM users WHERE username = '{username}' AND pass = '{password}'"

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()    
    cursor.execute(query)

    user = cursor.fetchone()
    conn.close()

    if user:
        message = f'Flag = {user[3]}'
    else:
        message = 'Invalid credentials'

    return render_template('index.html', results=message)


@app.route('/search', methods=['POST'])
def search():
    user_input = request.form['search_term']

    # Vulnerable SQL query
    #query = f\"SELECT * FROM users WHERE username = '{user_input}'\"
    query=f"SELECT * FROM users WHERE username = '{user_input}'"
    
    # Execute the query
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except sqlite3.Error as e:
        results = f'Error: {e}'

    conn.close()
    print("executed")
    if not results:
        print("REZ: ",results)
        return render_template('index.html', results2="User Doesn't exits.")
    else:
        print("res: ",results)
        return render_template('index.html', results2="User exits!")

if __name__ == '__main__':
    initDB()
    app.run(debug=True, host='0.0.0.0', port=80)
