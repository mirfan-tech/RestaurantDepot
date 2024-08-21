import os
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from fpdf import FPDF
from dotenv import load_dotenv
import sqlite3  # Use sqlite3 for local SQLite database handling
from azure.storage.blob import BlobServiceClient

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Azure Blob Storage settings
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = os.getenv('AZURE_CONTAINER_NAME')
blob_name = 'purchase_manager.db'

# Function to download .db from Azure Blob Storage
def download_blob():
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    download_file_path = os.path.join(os.getcwd(), blob_name)

    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    return download_file_path

orders = []

# Database connection parameters from .env file
DATABASE = 'purchase_manager.db'  # .db file name

# Function to fetch items from SQLite Database
DATABASE = download_blob()  # This downloads the database from Azure Blob Storage
def fetch_items_from_db():
    items_by_category = {}
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Items.ItemId, Items.ItemDescription, ItemCategory.CategoryName
            FROM Items
            JOIN ItemCategory ON Items.CategoryID = ItemCategory.CategoryID
        """)
        for row in cursor:
            item = {'id': row[0], 'name': row[1], 'category': row[2]}  
            category = row[2]
            if category not in items_by_category:
                items_by_category[category] = []
            items_by_category[category].append(item)
    return items_by_category

@app.route('/')
def index():
    items = fetch_items_from_db()  # Fetch items from SQLite database
    return render_template('index.html', items=items)

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    items_by_category = fetch_items_from_db()
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
        return redirect(url_for('index'))

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
