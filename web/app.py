from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Đường dẫn đến tệp CSV chứa thông tin người dùng
csv_file = "users.csv"

# Kiểm tra xem tệp CSV có tồn tại không
if not os.path.exists(csv_file):
    # Nếu không tồn tại, tạo một tệp trống
    df = pd.DataFrame(columns=["username","email", "password"])
    df.to_csv(csv_file, index=False)
    
# Hàm kiểm tra đăng nhập
def is_authenticated(email, password):
    users_df = pd.read_csv(csv_file)
    if (email in users_df["email"].values) and (
        password == users_df.loc[users_df["email"] == email]["password"].values[0]
    ):
        username = users_df.loc[users_df["email"] == email]["username"].values[0]
        return True, username
    return False, None
    

@app.route('/')
def index():
    # if 'email' in session:
    #     return render_template('index.html')
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'register' in request.form:
            # Nếu người dùng chọn đăng ký, chuyển hướng đến trang đăng ký
            return redirect(url_for('register'))

        email = request.form['email']  # Lấy email từ form
        password = request.form['password']

        authenticated, username = is_authenticated(email, password)

        if authenticated:
            session['email'] = email
            session['username'] = username  # Set the username in the session
            return redirect(url_for('index'))
        return 'Đăng nhập không thành công. <a href="/login">Thử lại</a>'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        users_df = pd.read_csv(csv_file)

        # Kiểm tra xem email đã tồn tại chưa
        if email in users_df["email"].values:
            return 'Email đã tồn tại. <a href="/register">Thử lại</a>'

        # Thêm người dùng mới vào tệp CSV
        new_user = pd.DataFrame({"username": [username],"email": [email], "password": [password]})
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        users_df.to_csv(csv_file, index=False)
        return 'Đăng ký thành công! <a href="/login">Đăng nhập</a>'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/products')
def products():
    if 'email' in session:
        return render_template('products.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
