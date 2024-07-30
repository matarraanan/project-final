from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pyrebase

app = Flask(__name__, template_folder="templates",static_folder="static")
app.secret_key = 'your_secret_key'

# Firebase configuration
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
#home route 
@app.route('/')
def home():
    who_r_u = session.get('who_r_u')  # Check if company or candidate
    users = db.child("Users").get().val()  # Get value of users dictionary in the DB
    signd = session.get('signed', False)  #check if u signed
    return render_template("homepage.html", are_u=who_r_u, users=users, signd=signd) 
    #returns the hompage with who u r, users and if u signed contract
@app.route('/signup', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        taz = request.form['taz']
        who_r_u = request.form['who']
        #get info from html
        try:
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = user
            
            usr_info = {"name": name, "taz": taz, "who_r_u": who_r_u, "signed": False}
            db.child("Users").child(user['localId']).set(usr_info)
            #make the user, save in session and db 
            session['who_r_u'] = who_r_u
            return redirect(url_for('home'))
        except:
            return redirect( url_for('error'))
    
    return render_template('sign-up.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try: #login 
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            user_info = db.child("Users").child(user['localId']).get().val()
            session['name'] = user_info['name']
            session['who_r_u'] = user_info['who_r_u']
            session['signed'] = user_info['signed']
            return redirect(url_for('home'))
        except:
            return redirect( url_for('error'))
    return render_template('sign-in.html') 
@app.route('/contract', methods=['GET'])
def contract():
    if session.get('who_r_u'):
        return render_template("contract.html" )
    else:
        return redirect(url_for('home'))
@app.route('/submit_signature', methods=['POST'])
def submit_signature():
    signature_data = request.form['signature']
    user_id = session['user']['localId']
    
    try:
        db.child("Users").child(user_id).update({"signed": True, "signature": signature_data})
        return redirect(url_for('thanks'))
    except:
        return redirect( url_for('error'))

@app.route('/user')
def user_list():
    who_r_u = session.get('who_r_u')
    if who_r_u == "company":
        users = db.child("Users").get().val()
        return render_template("users.html", users=users)
    else:
        return redirect(url_for('home'))

@app.route('/candidates', methods=['GET', 'POST'])
def candidates():
    who_r_u = session.get('who_r_u')
    if who_r_u == "candidate":
        return render_template("candidates.html")
    else:
        return redirect(url_for('home'))

@app.route('/prep', methods=['GET', 'POST'])
def prep():
    who_r_u = session.get('who_r_u')
    if who_r_u == "candidate":
        return render_template("interview.html")
    else:
        return redirect(url_for('home'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user", None)
    session.pop("who_r_u", None)
    session.pop("name", None)
    session.pop("signed", None)
    return redirect(url_for('home'))

@app.route('/user/<user_id>', methods=['GET'])
def user_detail(user_id):
    user = db.child("Users").child(user_id).get().val()
    return render_template("user_detail.html", user=user)

@app.route('/submit_interview')
def submit_interview():
  answer = request.form['message']
  try:
    session['message'] = answer
    return redirect(url_for('thanks'))
  except:
    return redirect(url_for('error'))

@app.route('/thanks')
def thanks ():
  return render_template("thanks.html")

@app.route('/error')
def error ():
  return render_template("error.html")

@app.route('/voicerec')
def voicerec():
  return render_template("voicerec.html")

if __name__ == '__main__':
    app.run(debug=True)
