FROM python:latest

RUN apt update

RUN apt install sqlite3

WORKDIR /usr/app/src/

RUN mkdir templates

RUN pip install flask

RUN pip install jinja2

RUN echo "from flask import Flask, render_template, request\nimport sqlite3, os\napp = Flask(__name__)\ndef initDB(): # check if table exists if not create it\n    db_file = 'example.db'\n    if not os.path.exists(db_file):\n        os.system('touch '+db_file)\n    conn = sqlite3.connect(db_file)\n    cursor = conn.cursor()\n    #create tables\n    cursor.execute('''\n            CREATE TABLE IF NOT EXISTS users (\n                id INTEGER PRIMARY KEY AUTOINCREMENT,\n                username TEXT NOT NULL,\n                pass TEXT NOT NULL,\n                flag TEXT NOT NULL\n            )\n        ''')\n    \n    cursor.execute('SELECT * FROM users WHERE username = \'admin\'')\n    existing_admin = cursor.fetchone()\n    if not existing_admin:\n        cursor.execute('INSERT OR IGNORE INTO users (username, pass, flag) VALUES (\'admin\', \'PassPhraseToNotForgetTheAdminLogin\', \'Ve$mkh@zUgM#6Zksci*P#PUheBNVHHMP&EpHLUTba3X**nGfC3#8wtVi\')')\n        conn.commit()\n    conn.close()\n@app.route('/')\ndef index():\n    return render_template('index.html')\n@app.route('/login', methods=['POST'])\ndef login():\n    username = request.form['username']\n    password = request.form['password']\n    #query = 'SELECT * FROM users WHERE username = '+username+' AND pass = '+password\n    query = f\"SELECT * FROM users WHERE username = '{username}' AND pass = '{password}'\"\n    conn = sqlite3.connect('example.db')\n    cursor = conn.cursor()\n    print(f'Executing query: {query}')\n    # Execute the vulnerable query\n    cursor.execute(query)\n    # Fetch results\n    user = cursor.fetchone()\n    # Close database connection\n    conn.close()\n    if user:\n        message = f'Flag = {user[3]}'\n    else:\n        message = 'Invalid credentials'\n    return render_template('search_result.html', results=message)\nif __name__ == '__main__':\n    initDB()\n    app.run(debug=True, host='0.0.0.0', port=80)\n" > app.py

RUN echo "<!DOCTYPE html>\n<html lang='en'>\n<head>\n    <meta charset='UTF-8'>\n    <meta http-equiv='X-UA-Compatible' content='IE=edge'>\n    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n    <title>SQL Injection Example</title>\n</head>\n<body>\n    <h1>Login SQL Inj</h1>\n    <form action='/login' method='post'>\n        <label for='username'>Username:</label>\n        <input type='text' id='username' name='username' required><br>\n        <label for='password'>Password:</label>\n        <input type='password' id='password' name='password' required>\n        <button type='submit'>Login</button>\n    </form>\n</body>\n</html>\n" > templates/index.html

RUN echo "<!DOCTYPE html>\n<html lang='en'>\n<head>\n    <meta charset='UTF-8'>\n    <meta http-equiv='X-UA-Compatible' content='IE=edge'>\n    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n    <title>Search Result</title>\n</head>\n<body>\n    <h1>Login SQL Inj</h1>\n    <form action='/login' method='post'>\n        <label for='username'>Username:</label>\n        <input type='text' id='username' name='username' required><br>\n      <label for='password'>Password:</label>\n        <input type='password' id='password' name='password' required>\n        <button type='submit'>Login</button>\n    </form>\n    <div>        \n        <h2>Result</h2>\n        <p>{{ results }}</p>\n    </div>\n</body>\n</html>\n" > templates/search_result.html

CMD ["python", "app.py"]
