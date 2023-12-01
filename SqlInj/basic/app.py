from flask import Flask, render_template, request
import sqlite3, os

app = Flask(__name__)

def initDB(): # check if table exists if not create it
    db_file = 'example.db'
    if not os.path.exists(db_file):
        os.system('touch '+db_file)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    #create tables
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                pass TEXT NOT NULL,
                flag TEXT NOT NULL
            )
        ''')
    
    cursor.execute('SELECT * FROM users WHERE username = \'admin\'')
    existing_admin = cursor.fetchone()
    if not existing_admin:
        cursor.execute('INSERT OR IGNORE INTO users (username, pass, flag) VALUES (\'admin\', \'PassPhraseToNotForgetTheAdminLogin\', \'Ve$mkh@zUgM#6Zksci*P#PUheBNVHHMP&EpHLUTba3X**nGfC3#8wtVi\')')
        conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']


    #query = 'SELECT * FROM users WHERE username = '+username+' AND pass = '+password
    query = f\"SELECT * FROM users WHERE username = '{username}' AND pass = '{password}'\"

    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    print(f'Executing query: {query}')
    # Execute the vulnerable query
    cursor.execute(query)

    # Fetch results
    user = cursor.fetchone()

    # Close database connection
    conn.close()

    if user:
        message = f'Flag = {user[3]}'
    else:
        message = 'Invalid credentials'


    return render_template('search_result.html', results=message)

if __name__ == '__main__':
    initDB()
    app.run(debug=True, host='0.0.0.0', port=80)
