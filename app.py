import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_this_in_production'
DB_NAME = 'wood_manufacturing.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        with open('schema.sql') as f:
            conn.executescript(f.read())
        conn.close()
        print("Database initialized.")

# --- Helpers ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- User Routes ---

@app.route('/')
def index():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    wood_types = conn.execute('SELECT * FROM wood_types').fetchall()
    
    # Get all subtypes and group them by type_id for easier JS handling if needed, 
    # but strictly for the form, we might fetch them dynamically or pass all.
    # Let's pass all active data for the calculator.
    labor_cost = conn.execute('SELECT amount FROM labor_cost WHERE id = 1').fetchone()
    labor_amount = labor_cost['amount'] if labor_cost else 0
    
    conn.close()
    return render_template('index.html', products=products, wood_types=wood_types, labor_cost=labor_amount)

@app.route('/get_subtypes/<int:type_id>')
def get_subtypes(type_id):
    conn = get_db_connection()
    subtypes = conn.execute('SELECT * FROM wood_subtypes WHERE type_id = ?', (type_id,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in subtypes])

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    conn = get_db_connection()
    product = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    wood_types = conn.execute('SELECT * FROM wood_types').fetchall()
    labor_cost = conn.execute('SELECT amount FROM labor_cost WHERE id = 1').fetchone()
    labor_amount = labor_cost['amount'] if labor_cost else 0
    conn.close()
    
    if product is None:
        return redirect(url_for('index'))
        
    return render_template('product_detail.html', product=product, wood_types=wood_types, labor_cost=labor_amount)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    width = float(data.get('width', 0))
    height = float(data.get('height', 0))
    subtype_id = data.get('subtype_id')
    product_id = data.get('product_id') # Optional product ID
    
    conn = get_db_connection()
    subtype = conn.execute('SELECT * FROM wood_subtypes WHERE id = ?', (subtype_id,)).fetchone()
    labor_cost_row = conn.execute('SELECT amount FROM labor_cost WHERE id = 1').fetchone()
    labor_cost = labor_cost_row['amount'] if labor_cost_row else 0
    
    product_base_price = 0
    if product_id:
        product = conn.execute('SELECT base_price FROM products WHERE id = ?', (product_id,)).fetchone()
        if product:
            product_base_price = product['base_price']
            
    conn.close()
    
    if not subtype:
        return jsonify({'error': 'Invalid wood subtype'}), 400
        
    wood_rate = subtype['price_per_sqft']
    total_area = width * height
    wood_cost = total_area * wood_rate
    total_cost = wood_cost + labor_cost + product_base_price
    
    return jsonify({
        'area': round(total_area, 2),
        'wood_rate': wood_rate,
        'wood_cost': round(wood_cost, 2),
        'labor_cost': labor_cost,
        'base_price': product_base_price,
        'total_cost': round(total_cost, 2)
    })

# --- Admin Routes ---

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple hardcoded credentials for prototype
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    conn = get_db_connection()
    wood_types = conn.execute('SELECT * FROM wood_types').fetchall()
    subtypes = conn.execute('SELECT s.*, w.name as wood_name FROM wood_subtypes s JOIN wood_types w ON s.type_id = w.id').fetchall()
    products = conn.execute('SELECT * FROM products').fetchall()
    labor_cost = conn.execute('SELECT amount FROM labor_cost WHERE id = 1').fetchone()
    
    stats = {
        'wood_types': len(wood_types),
        'subtypes': len(subtypes),
        'products': len(products)
    }
    
    # Convert Rows to dicts for JSON serialization in template
    wood_types = [dict(row) for row in wood_types]
    subtypes = [dict(row) for row in subtypes]
    products = [dict(row) for row in products]
    
    conn.close()
    return render_template('admin_dashboard.html', 
                         wood_types=wood_types, 
                         subtypes=subtypes, 
                         products=products,
                         labor_cost=labor_cost,
                         stats=stats)

# --- CRUD Operations ---

# Wood Type CRUD
@app.route('/admin/wood/add', methods=['POST'])
@login_required
def add_wood():
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('INSERT INTO wood_types (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()
    flash('Wood type added successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/wood/delete/<int:id>')
@login_required
def delete_wood(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM wood_types WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Wood type deleted')
    return redirect(url_for('admin_dashboard'))

# Subtype CRUD
@app.route('/admin/subtype/add', methods=['POST'])
@login_required
def add_subtype():
    type_id = request.form['type_id']
    name = request.form['name']
    price = request.form['price']
    
    conn = get_db_connection()
    conn.execute('INSERT INTO wood_subtypes (type_id, name, price_per_sqft) VALUES (?, ?, ?)',
                 (type_id, name, price))
    conn.commit()
    conn.close()
    flash('Subtype added successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/subtype/delete/<int:id>')
@login_required
def delete_subtype(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM wood_subtypes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Subtype deleted')
    return redirect(url_for('admin_dashboard'))

# Labor Cost Update
@app.route('/admin/labor/update', methods=['POST'])
@login_required
def update_labor():
    amount = request.form['amount']
    conn = get_db_connection()
    conn.execute('UPDATE labor_cost SET amount = ? WHERE id = 1', (amount,))
    conn.commit()
    conn.close()
    flash('Labor cost updated')
    return redirect(url_for('admin_dashboard'))

# Product CRUD
@app.route('/admin/product/add', methods=['POST'])
@login_required
def add_product():
    name = request.form['name']
    image_url = request.form['image_url']
    description = request.form['description']
    base_price = request.form.get('base_price', 0)
    
    conn = get_db_connection()
    conn.execute('INSERT INTO products (name, image_url, description, base_price) VALUES (?, ?, ?, ?)',
                 (name, image_url, description, base_price))
    conn.commit()
    conn.close()
    flash('Product added successfully')
    return redirect(url_for('admin_dashboard'))

# --- Update Routes ---

@app.route('/admin/wood/update', methods=['POST'])
@login_required
def update_wood():
    id = request.form['id']
    name = request.form['name']
    conn = get_db_connection()
    conn.execute('UPDATE wood_types SET name = ? WHERE id = ?', (name, id))
    conn.commit()
    conn.close()
    flash('Wood type updated')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/subtype/update', methods=['POST'])
@login_required
def update_subtype():
    id = request.form['id']
    name = request.form['name']
    price = request.form['price']
    type_id = request.form['type_id']
    
    conn = get_db_connection()
    conn.execute('UPDATE wood_subtypes SET name = ?, price_per_sqft = ?, type_id = ? WHERE id = ?',
                 (name, price, type_id, id))
    conn.commit()
    conn.close()
    flash('Sub-type updated')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/product/update', methods=['POST'])
@login_required
def update_product():
    id = request.form['id']
    name = request.form['name']
    image_url = request.form['image_url']
    description = request.form['description']
    base_price = request.form.get('base_price', 0)
    
    conn = get_db_connection()
    conn.execute('UPDATE products SET name = ?, image_url = ?, description = ?, base_price = ? WHERE id = ?',
                 (name, image_url, description, base_price, id))
    conn.commit()
    conn.close()
    flash('Product updated')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/product/delete/<int:id>')
@login_required
def delete_product(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Product deleted')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
