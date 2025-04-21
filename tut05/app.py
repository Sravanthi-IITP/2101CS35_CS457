from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import init_db
from models import User

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for security


mysql = init_db(app)

# Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    data = cur.fetchone()
    cur.close()

    if data:
        return User(id=data['id'], username=data['username'], password_hash=data['password_hash'], role=data['role'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = 'viewer'  # Default role

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)", (username, password, role))
        mysql.connection.commit()
        cur.close()

        flash("Registered successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        data = cur.fetchone()
        cur.close()

        if data and check_password_hash(data['password_hash'], password):
            user = User(id=data['id'], username=data['username'], password_hash=data['password_hash'], role=data['role'])
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!", "danger")

    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', role=current_user.role)

@app.route('/assign_role', methods=['GET', 'POST'])
@login_required
def assign_role():
    if current_user.role != 'admin':
        flash("Access denied!", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET role = %s WHERE username = %s", (role, username))
        mysql.connection.commit()
        cur.close()
        flash("Role updated successfully!", "success")
        return redirect(url_for('dashboard'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT username, role FROM users")
    users = cur.fetchall()
    cur.close()
    return render_template('assign_role.html', users=users)

@app.route('/view_data')
@login_required
def view_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stud_info")
    students = cur.fetchall()
    cur.close()
    return render_template('view_data.html', students=students)

@app.route('/edit_data', methods=['GET', 'POST'])
@login_required
def edit_data():
    if current_user.role not in ['admin', 'editor']:
        flash("You do not have permission to edit data!", "danger")
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        roll = request.form['roll']
        name = request.form['name']
        age = request.form['age']
        branch = request.form['branch']
        hometown = request.form['hometown']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE stud_info SET name=%s, age=%s, branch=%s, hometown=%s WHERE roll=%s",
                    (name, age, branch, hometown, roll))
        mysql.connection.commit()
        cur.close()
        flash("Record updated successfully!", "success")
        return redirect(url_for('view_data'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stud_info")
    students = cur.fetchall()
    cur.close()
    return render_template('edit_data.html', students=students)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
