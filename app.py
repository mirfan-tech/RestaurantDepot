import os
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from fpdf import FPDF
from dotenv import load_dotenv
import pyodbc

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

orders = []

# Database connection parameters from .env file
server = os.getenv('AZURE_SERVER')
database = os.getenv('AZURE_DATABASE')
username = os.getenv('AZURE_USERNAME')
password = os.getenv('AZURE_PASSWORD')
driver = '{ODBC Driver 18 for SQL Server}'

# Function to fetch items from Azure SQL Database
def fetch_items_from_db():
    items_by_category = {}  # Initialize the dictionary here
    with pyodbc.connect(f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ItemID, ItemName, Category FROM Items")  # Adjust SQL query as needed
        for row in cursor:
            item = {'id': row[0], 'name': row[1], 'category': row[2]}
            category = row[2]
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append(item)
    return items_by_category

@app.route('/')
def index():
    items = fetch_items_from_db()  # Fetch items from database
    return render_template('index.html', items=items)

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    items_by_category = fetch_items_from_db()  # Fetch categorized items from the database
    item = None
    for items_list in items_by_category.values():
        for i in items_list:
            if i['id'] == item_id:
                item = i
                break
        if item:
            break
    
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        quantity = request.form.get('quantity')
        orders.append({'item': item, 'quantity': int(quantity)})
        return redirect(url_for('index'))  # Redirect back to the main list

    return render_template('item_detail.html', item=item)

@app.route('/clear-list', methods=['POST'])
def clear_list():
    global orders
    orders = []
    return jsonify({'success': True})


@app.route('/update-quantity/<int:item_id>', methods=['POST'])
def update_quantity(item_id):
    action = request.json['action']
    new_quantity = 0

    for order in orders:
        if order['item']['id'] == item_id:
            if action == 'increment':
                order['quantity'] += 1
            elif action == 'decrement' and order['quantity'] > 0:
                order['quantity'] -= 1
            elif action == 'delete':
                orders.remove(order)
                new_quantity = 0
                break
            new_quantity = order['quantity']
            break
    
    return jsonify({'newQuantity': new_quantity})

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
