from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('ecommerce.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/users')
def search_users():
    search = request.args.get('search', '')  # get search keyword, default empty string
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT id, first_name, last_name, email FROM users
        WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
    """
    like_pattern = f"%{search}%"
    cursor.execute(query, (like_pattern, like_pattern, like_pattern))
    users = cursor.fetchall()
    conn.close()

    results = []
    for user in users:
        results.append({
            'id': user['id'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email']
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/users/<int:user_id>/orders')
def get_user_orders(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT order_id, status, created_at FROM orders
        WHERE user_id = ?
    """
    cursor.execute(query, (user_id,))
    orders = cursor.fetchall()
    conn.close()

    results = []
    for order in orders:
        results.append({
            'order_id': order['order_id'],
            'status': order['status'],
            'created_at': order['created_at']
        })

    return jsonify(results)
@app.route('/users/<int:user_id>/orders')
def get_orders(user_id):
    orders = query_db("SELECT id, order_date, status FROM orders WHERE user_id = ?", (user_id,))
    result = [{'id': o[0], 'order_date': o[1], 'status': o[2]} for o in orders]
    return jsonify(result)

@app.route('/orders/<int:order_id>/items')
def get_order_items(order_id):
    items = query_db("""
        SELECT p.name, oi.quantity, oi.price 
        FROM order_items oi
        JOIN products p ON oi.product_id = p.id
        WHERE oi.order_id = ?""", (order_id,))
    result = [{'product_name': i[0], 'quantity': i[1], 'price': i[2]} for i in items]
    return jsonify(result)
if __name__ == '__main__':
    app.run(debug=True)
