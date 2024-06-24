import os
import pyodbc
from flask import Flask, render_template, request, redirect, url_for, send_file
from fpdf import FPDF
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Flask app setup
app = Flask(__name__)

orders = []

# Database connection string
DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

if not all([DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("Some environment variables are missing")

connection_string = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_SERVER};DATABASE={DB_NAME};'
    f'UID={DB_USER};PWD={DB_PASSWORD};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30'
)

def get_db_connection():
    return pyodbc.connect(connection_string)

def fetch_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT category, id, name FROM dbo.items")
    rows = cursor.fetchall()
    items = {}
    for row in rows:
        category = row[0]
        item = {'id': row[1], 'name': row[2]}
        if category in items:
            items[category].append(item)
        else:
            items[category] = [item]
    conn.close()
    return items

@app.route('/')
def index():
    items = fetch_items()
    return render_template('index.html', items=items)

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    items = fetch_items()
    item = None
    for category, items_list in items.items():
        item = next((i for i in items_list if i['id'] == item_id), None)
        if item:
            break
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        orders.append({'item': item, 'quantity': quantity})
        return redirect(url_for('index'))  # Redirect back to the main list
    return render_template('item_detail.html', item=item)

@app.route('/summary')
def order_summary():
    return render_template('order_summary.html', orders=orders)

@app.route('/generate_pdf')
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for order in orders:
        pdf.cell(200, 10, txt=f"{order['item']['name']} - {order['quantity']}", ln=True)
    pdf_output = "order_summary.pdf"
    pdf.output(pdf_output)
    return send_file(pdf_output, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
