from MySQLdb import IntegrityError
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import bcrypt
app = Flask(__name__)

# Configure MySQL Database
app.config['MYSQL_HOST'] = 'localhost'  # MySQL host (e.g., localhost)
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = ''  # MySQL password
app.config['MYSQL_DB'] = 'crud_demo'  # Database name

mysql = MySQL(app)

# Initialize table
def create_table():
    with app.app_context():  # Ensure application context
        cursor = mysql.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS user (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(80) UNIQUE NOT NULL,
                            password VARCHAR(120) NOT NULL,
                            active BOOLEAN DEFAULT TRUE)''')
        mysql.connection.commit()
        cursor.close()

# Create User
@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    active = data.get('active', True)

    # Validate inputs
    if not username or not password:
        return jsonify({"error": "Username and password are required!"}), 400

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters long!"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long!"}), 400

    try:
        # Hash the password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

        # Insert user into the database
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO user (username, password, active) VALUES (%s, %s, %s)',
                       (username, hashed_password.decode('utf-8'), active))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "User created successfully!"}), 201

    except IntegrityError as e:
        # Handle duplicate username error
        if "Duplicate entry" in str(e):
            return jsonify({"error": "Username already exists!"}), 409
        else:
            return jsonify({"error": "Database error occurred!"}), 500

    except Exception as e:
        # Handle any other unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Get User
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM user WHERE id = %s', [id])
    user = cursor.fetchone()
    cursor.close()

    if user:
        return jsonify({"id": user[0], "username": user[1], "active": user[3]})
    else:
        return jsonify({"message": "User not found!"}), 404

# Update User
@app.route('/user/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    active = data.get('active')

    # Validate inputs
    if not username and not password and active is None:
        return jsonify({"error": "At least one field (username, password, or active) must be provided!"}), 400

    if username and len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters long!"}), 400

    if password and len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters long!"}), 400

    try:
        cursor = mysql.connection.cursor()

        # Check if user exists
        cursor.execute('SELECT * FROM user WHERE id = %s', [id])
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found!"}), 404

        # Prepare the fields to update
        updates = []
        params = []
        if username:
            # Check if the new username is already taken by another user
            cursor.execute('SELECT * FROM user WHERE username = %s AND id != %s', (username, id))
            if cursor.fetchone():
                return jsonify({"error": "Username already exists!"}), 409
            updates.append('username = %s')
            params.append(username)
        if password:
            # Hash the password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            updates.append('password = %s')
            params.append(hashed_password.decode('utf-8'))
        if active is not None:
            updates.append('active = %s')
            params.append(active)

        # Execute the update query
        if updates:
            query = f"UPDATE user SET {', '.join(updates)} WHERE id = %s"
            params.append(id)
            cursor.execute(query, params)
            mysql.connection.commit()

        cursor.close()

        return jsonify({"message": "User updated successfully!"}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# Delete User
@app.route('/user/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        cursor = mysql.connection.cursor()

        # Check if the user exists
        cursor.execute('SELECT * FROM user WHERE id = %s', [id])
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "Invalid user ID. User not found!"}), 404

        # Delete the user if found
        cursor.execute('DELETE FROM user WHERE id = %s', [id])
        mysql.connection.commit()
        cursor.close()

        return jsonify({"message": "User deleted successfully!"}), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
@app.route('/users', methods=['GET'])
def list_users():
    try:
        # Get pagination parameters from the query string
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        if page < 1 or per_page < 1:
            return jsonify({"error": "Page and per_page must be positive integers!"}), 400

        offset = (page - 1) * per_page  # Calculate the offset for SQL query

        cursor = mysql.connection.cursor()

        # Count total users
        cursor.execute('SELECT COUNT(*) FROM user')
        total_users = cursor.fetchone()[0]

        # Fetch paginated users
        cursor.execute('SELECT id, username, active FROM user LIMIT %s OFFSET %s', (per_page, offset))
        users = cursor.fetchall()

        # Close the cursor
        cursor.close()

        # Prepare the response
        user_list = [{"id": user[0], "username": user[1], "active": user[2]} for user in users]
        response = {
            "page": page,
            "per_page": per_page,
            "total_users": total_users,
            "total_pages": (total_users + per_page - 1) // per_page,  # Round up division
            "users": user_list
        }

        return jsonify(response), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    create_table()  # Ensure table is created before starting the app
    app.run(debug=True)
