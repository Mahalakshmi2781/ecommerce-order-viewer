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
