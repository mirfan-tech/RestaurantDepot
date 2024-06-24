import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from fpdf import FPDF
import os
from items import items  # Import the categorized items list

app = Flask(__name__)

orders = []

@app.route('/')
def index():
    return render_template('index.html', items=items)

@app.route('/item/<int:item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
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

