from flask import Flask, render_template, request

app = Flask(__name__)

# Dữ liệu mẫu của người dùng (trong thực tế, bạn cần sử dụng cơ sở dữ liệu)
users = []

@app.route('/')
def home():
    return render_template('products.html')

if __name__ == '__main__':
    app.run(debug=True)
