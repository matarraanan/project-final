from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase

app = Flask(__name__, template_folder="templates")
app.secret_key = 'your_secret_key'  

firebaseConfig = {
  "apiKey": "AIzaSyDt8zwi8pYNbfpHnhQRl3qrrmPwRItHUgk",
  "authDomain": "cons-project-3d67b.firebaseapp.com",
  "projectId": "cons-project-3d67b",
  "storageBucket": "cons-project-3d67b.appspot.com",
  "messagingSenderId": "1002166356174",
  "appId": "1:1002166356174:web:3e7886cfe4c944c4b1a89f",
  "databaseURL": "https://cons-project-3d67b-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/')
def home():
    who_r_u = session.get('who_r_u')
    return render_template("homepage.html", ar_u=who_r_u)

@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        taz = request.form['taz']
        who_r_u = request.form['who']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = user
            usr_info = {"name": name, "taz": taz}
            db.child("Users").child(user['localId']).set(usr_info)
            session['who_r_u'] = who_r_u
            return redirect(url_for('home'))
        except:
            return "error"
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
