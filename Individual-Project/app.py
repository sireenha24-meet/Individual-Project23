from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
   "apiKey": "AIzaSyB9XqI5tB9MK31aOzHhTDcMsXx_IhyzvDE",
  "authDomain": "cs-individual-project-ac39b.firebaseapp.com",
  "projectId": "cs-individual-project-ac39b",
  "storageBucket": "cs-individual-project-ac39b.appspot.com",
  "messagingSenderId": "1039855906811",
  "appId": "1:1039855906811:web:582855fd65a6a57eec655e",
  "databaseURL": "https://cs-individual-project-ac39b-default-rtdb.europe-west1.firebasedatabase.app/"
};
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/index',methods=['GET', 'POST'])
def Index():
    if request.method=='POST':
        animal=request.form['animal']
        topic=request.form['topic']
        sport=request.form['sport']
        food=request.form['food']
        brand=request.form['brand']
        gum=request.form['gum']
        country=request.form['country']
        survey = {"survey":{"animal":animal,"topic":topic,"sport":sport,"food":food,"brand":brand,"gum":gum,"country":country}}
        db.child("Users").child(login_session['user']['localId']).update(survey)
    return render_template('index.html')



@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('Index'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #full_name = request.form['full_name']
        #username = request.form['username'] 

        try:
            user={"name":full_name, "email":email}
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID=login_session['user']['localId']
            db.child("Users").child(UID).set(user)
            return redirect(url_for('Index'))
        except:
            error = "Authentication failed"
    return render_template("signup.html")

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/results')
def results():
    return render_template("results.html")


#dictionary={"staff":{"Jihad":['2','1','1','2','3','2','3'] , "George":['2','1','2','1','3','1','3'] , "Kenda":[] , "Jameel":['1','1','1','2','3','2','2'] , "Ava":['2','1','1','1','2','1','3'] , "Ali":[] , "Fouad":[]}}
#c=0
#c1=0
#c2=0
#animal=request.form['animal']
#topic=request.form['topic']
#sport=request.form['sport']
#food=request.form['food']
#brand=request.form['brand']
#gum=request.form['gum']
#country=request.form['country']
#survey = {"survey":{"animal":animal,"topic":topic,"sport":sport,"food":food,"brand":brand,"gum":gum,"country":country}}
#list=['JIHAD','GEORGE','KENDA','JAMEEL','AVA','ALI','FOUAD']
#def Result():
   #for i in range(7):
        #for j in range(7):
            #if dictionary['staff'][i][j]==survey['survey'][j]:
                #c++

        #for l in range(7):
            #if dictionary['staff'][l].append(c)

    #for n in range(7):
        #if dictionary['staff'][n][7]>c1:
            #c2=n
            #c1=dictionray['staff'][n][7]


    #return return render_template("results.html",'You're most similar to 'list[c2])      

                







if __name__ == '__main__':
    app.run(debug=True)