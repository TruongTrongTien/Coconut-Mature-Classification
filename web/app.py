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
    return (email in users_df["email"].values) and (
        password == users_df.loc[users_df["email"] == email]["password"].values[0]
    )
    

@app.route('/')
def index():
    if 'email' in session:
        return f"Xin chào, {session['email']}! <a href='/logout'>Đăng xuất</a> <a href='/products'>Sản Phẩm</a>"
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

        users_df = pd.read_csv(csv_file)

        # Kiểm tra xem kết hợp email và mật khẩu có chính xác không
        if users_df[(users_df['email'] == email) & (users_df['password'] == password)].shape[0] > 0:
            session['email'] = email
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
    session.pop('email', None)
    return redirect(url_for('index'))

@app.route('/products')
def products():
    if 'email' in session:
        return render_template('products.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
