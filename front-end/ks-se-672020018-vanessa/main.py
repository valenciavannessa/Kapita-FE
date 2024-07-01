from flask import Flask, render_template, url_for, redirect, request, session, flash
import requests


app = Flask(__name__)

app.secret_key = 'abcd1234'

@app.route("/index")
def index():
    if "user" in session:
        # Ambil data dari API
        try:
            data = requests.get('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/products')
        except Exception as e:
            print("ERROR | Get products data |", e)

        return render_template("index.html", user=session["user"], products=data.json())
    else:
        return redirect(url_for('login'))

@app.route("/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Ambil data dari API
        try:
            admins = requests.get('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/admins')
        except Exception as e:
            print("ERROR | Get products data |", e)

        for user in admins.json():
            if user["username"] == username:
                if password == user['password']:
                    session["user"] = user["name"]
                    return redirect(url_for('index'))
                else:
                    flash("Login failed", category='error')
            else:
                flash('Username not registered', category='error')
    return render_template('login.html')

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

@app.route("/produk", methods=['GET'])
def produk():
    if "user" in session:
        # Ambil data dari API
        try:
            data = requests.get('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/produk')
        except Exception as e:
                print("ERROR | Get products data |", e)

        return render_template('produk.html', user=session["user"], produk=data.json())
    else:
        return redirect(url_for('login'))

    
@app.route("/pengguna")
def pengguna():
    if "user" in session:
        # Ambil data dari API
        try:
            data = requests.get('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/pengguna')
        except Exception as e:
            print("ERROR | Get users data |", e)

        return render_template('pengguna.html', user=session["user"], pengguna=data.json())
    else:
        return redirect(url_for('login'))

    
@app.route("/transaksi")
def transaksi():
    if "user" in session:
        # Ambil data dari API
        try:
            data = requests.get('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/transaksi')
        except Exception as e:
            print("ERROR | Get transaksi data |", e)

        return render_template('transaksi.html', user=session["user"], transaksi=data.json())
    else:
        return redirect(url_for('login'))


@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/edituser", methods=['GET', 'POST'])
def edituser():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     # name = request.form['name']
    #     # password = request.form['password']
    #     # email = request.form['email']
    #     # date = request.form['birthdate']
    #     # point = request.form['point']

    #     # Ambil data dari API
    #     try:
    #         eduser = requests.get('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/users')
    #     except Exception as e:
    #         print("ERROR | Get user data |", e)

    #     for user in eduser.json():
    #         if user["username"] == username:
    #             session["user"] = user["name"]
    #             session["username"] = user["username"]
    #             session["name"] = user["name"]
    #             session["pass"] = user["password"]
    #             session["email"] = user["email"]
    #             session["date"] = user["birthdate"]
    #             session["point"] = user["point"]
    #         else:
    #             flash('Username not registered', category='error')
    return render_template('edituser.html', user=session["user"])


@app.route("/editproduk<id_product>", methods=['GET', 'POST'])
def editproduk(id_product):
    if "user" in session:
        if request.method == 'POST':
            name_product = request.form['name_product']
            price = request.form['price']
            category = request.form['category']
            stock = request.form['stock']
            desc = request.form['desc']
                

            requests.post('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/editproduk', json=(name_product, price, category, stock, desc))
            
        return redirect(url_for('produk'))
    else:
        return redirect(url_for('login'))


@app.route("/updateproduk", methods=['GET'])
def updateproduk():
    if "user" in session:
        return render_template("editproduk.html", user=session["user"])
    else:
        return redirect(url_for('login'))

@app.route("/delete/<id_product>", methods=['POST', 'DELETE'])
def delete(id_product):
    # id = request.form['id_product']
    print(id_product)
    # requests.delete(f'http://127.0.0.1:5000/hapusproduk/{id}')
    requests.delete('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/hapusproduk', json={id_product})

    return redirect(url_for('produk'))


@app.route("/tambahproduk", methods=['GET', 'POST'])
def tambahproduk():
    if "user" in session:
            id_product = request.form['id_product']
            name_product = request.form['name_product']
            price = request.form['price']
            category = request.form['category']
            stock = request.form['stock']
            desc = request.form['desc']

            requests.post('https://backend-vanessa-5zn7xh2gqq-et.a.run.app/tambahproduk', json=(id_product, name_product, price, category, stock, desc))
        
            return redirect(url_for('produk'))
    else:
        return redirect(url_for('login'))

@app.route("/addproduk", methods=['GET'])
def addproduk():
    if "user" in session:
        return render_template("insertproduk.html", user=session["user"])
    else:
        return redirect(url_for('login'))

@app.route("/inserttransaksi", methods=['GET', 'POST'])
def inserttransaksi():
    return render_template('inserttransaksi.html', user=session["user"])

@app.route("/insertuser", methods=['GET', 'POST'])
def insertuser():
    return render_template('insertuser.html', user=session["user"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)