from flask import Flask, render_template
import sqlite3, os

app = Flask(__name__, static_folder='/app/data')

@app.route('/')
def index():
    # Connect to the database and execute a query
    conn = sqlite3.connect(os.path.join('data','images.db'))
    c = conn.cursor()
    c.execute('SELECT * FROM images')
    data = c.fetchall()
    conn.close()

    # Render the template with the data
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
