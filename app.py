from flask import Flask, send_from_directory, render_template
from flask import request, redirect, flash
from pymongo import MongoClient

app = Flask(__name__)

app.secret_key = 'key'
client = MongoClient('mongodb://localhost:27017')
db = client.users

@app.route('/', methods=['GET', 'POST'])
def login_user():
    if request.method == "GET":
        return render_template('login.html')
    if request.method == "POST":
        user = request.form['user']
        password = request.form['pwd']
        result = db.info.find_one({"user_db":user})
        try:
            if password == result["pass"]:
                return redirect('cabinet')
        except:
            e = "user and password not exist"
    return render_template('login.html')

@app.route('/register')
def register():
        return render_template('register.html')

@app.route('/cabinet')
def cabinet():
    return render_template('index.html')

@app.route('/addUserDb', methods=['POST'])
def addUserMongoDatabase():
    e = request.form['email_addr']
    pwd = request.form['pwd']
    user = request.form['user']
    db.info.insert({"user_db": user, "pass": pwd, "email": e})
    return render_template('login.html',user = user)

@app.errorhandler(404)
def error404(error):
    return '<h1>404 : page not found!</h1>', 404

@app.errorhandler(403)
def error404(error):
    return '<h1>403 : Acess forbiden</h1>', 403

@app.route('/img/<path:filename>')
def imgFile(filename):
    return send_from_directory('/static/img', filename)

@app.route('/static/css/<string:stylesheet>')
def css(stylesheet):
    return send_from_directory('static/css', stylesheet)

if __name__ == "__main__":
    print(db)
    app.run(debug=True)
