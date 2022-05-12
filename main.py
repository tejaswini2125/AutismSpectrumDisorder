#-----------------------------------------------extra_modules-----------------------------------------------------------
import os

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

filenumber = int(os.listdir('saved_conversations')[-1])
filenumber = filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.write('bot : Hi There! I am a medical chatbot. You can begin conversation by typing in a message and pressing enter.\n')
file.close()

#app = Flask(__name__)

english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                         {
                            'import_path': 'chatterbot.logic.BestMatch'
                         },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)
#-------------------------------------------------model_code------------------------------------------------------------
from random import random
import pandas as pd
data = pd.read_csv('data.csv')
from sklearn import preprocessing
le = preprocessing.LabelEncoder()

age = le.fit_transform(data.age)
gender = le.fit_transform(data.gender)
ethnicity = le.fit_transform(data.ethnicity)
jaundice = le.fit_transform(data.jaundice)
austim = le.fit_transform(data.austim)
country_of_res = le.fit_transform(data.country_of_res)
used_app_before = le.fit_transform(data.used_app_before)
age_desc = le.fit_transform(data.age_desc)
relation = le.fit_transform(data.relation)
class1 = le.fit_transform(data.class1)

testing = data

testing['age'] = age
testing['gender'] = gender
testing['ethnicity'] = ethnicity
testing['jaundice'] = jaundice
testing['austim'] = austim
testing['country_of_res'] = country_of_res
testing['used_app_before'] = used_app_before
testing['age_desc'] = age_desc
testing['relation'] = relation
testing['class1'] = class1

from sklearn.model_selection import train_test_split

X = data.drop('class1',axis=1)
y = data['class1']

X_train , X_test , y_train , y_test = train_test_split(X,y,test_size=.20,random_state=100)

from sklearn import svm
sv = svm.SVC(kernel='linear')
sv.fit(X_train,y_train)

y_pred_svm = sv.predict(X_test)
from sklearn.metrics import accuracy_score
score = round(accuracy_score(y_pred_svm,y_test)*100)

#-----------------------navies bayes------------------------------------
import sklearn
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from sklearn.metrics import accuracy_score

BernNB = BernoulliNB(binarize=.1)
BernNB.fit(X_train,y_train)
print(BernNB)
y_expect = y_test
y_pred = BernNB.predict(X_test)
print(accuracy_score(y_expect,y_pred)*100)

#---------------------navies bayes


#-------------------------------------------------model_code------------------------------------------------------------
#-------------
#
# -----------------------------------database---------------------------------------------------------------
import sqlite3
conn = sqlite3.connect('autism_database')
cur = conn.cursor()
try:
   cur.execute('''CREATE TABLE user (
     name varchar(20) DEFAULT NULL,
      email varchar(50) DEFAULT NULL,
     password varchar(20) DEFAULT NULL,
     gender varchar(10) DEFAULT NULL,
     age int(11) DEFAULT NULL
   )''')

except:
   pass
#------------------------------------------------database---------------------------------------------------------------
from flask import Flask,render_template, url_for,request, flash, redirect, session
app = Flask(__name__)
app.config['SECRET_KEY'] = '881e69e15e7a528830975467b9d87a98'
#-------------------------------------home_page-------------------------------------------------------------------------
@app.route('/')
@app.route('/home')
def home():
   if not session.get('logged_in'):
      return render_template('home.html')
   else:
      return redirect(url_for('user_account'))

@app.route('/home1')
def home1():
   if not session.get('logged_in'):
      return render_template('home1.html')
   else:
      return redirect(url_for('user_account'))

#-------------------------------------home_page-------------------------------------------------------------------------

#-------------------------------------about_page-------------------------------------------------------------------------
@app.route("/about")
def about():
   return render_template('about.html')
#-------------------------------------about_page-------------------------------------------------------------------------
@app.route("/sugesstion")
def sugesstion():
   return render_template('sugesstion.html')


@app.route("/sugesstion1")
def sugesstion1():
   return render_template('sugesstion1.html')

@app.route("/sugesstion2")
def sugesstion2():
   return render_template('sugesstion2.html')
#-------------------------------------user_login_page-------------------------------------------------------------------------
@app.route('/user_login',methods = ['POST', 'GET'])
def user_login():
   conn = sqlite3.connect('autism_database')
   cur = conn.cursor()
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['psw']
      print('asd')
      count = cur.execute('SELECT * FROM user WHERE email = "%s" AND password = "%s"' % (email, password))
      print(count)
      #conn.commit()
      #cur.close()
      l = len(cur.fetchall())
      if l > 0:
         flash( f'Successfully Logged in' )
         return render_template('user_account.html')
      else:
         print('hello')
         flash( f'Invalid Email and Password!' )
   return render_template('user_login.html')

# -------------------------------------user_login_page-----------------------------------------------------------------

# -----------------------------------predict_page-----------------------------------------------------------------

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    global BernNB
    A1_Score = request.form['A1_Score']
    A2_Score = request.form['A2_Score']
    A3_Score = request.form['A3_Score']
    A4_Score = request.form['A4_Score']
    A5_Score = request.form['A5_Score']
    A6_Score = request.form['A6_Score']
    A7_Score = request.form['A7_Score']
    A8_Score = request.form['A8_Score']
    A9_Score = request.form['A9_Score']
    A10_Score = request.form['A10_Score']
    age = request.form['age']
    gender = request.form['sex']
    if gender == 'male':
        gender = 1
    else:
        gender = 0
    ethnicity = request.form['ethnicity']
    jaundice = request.form['jaundice']
    if jaundice == 'yes':
        jaundice = 1
    else:
        jaundice = 0
    austim = request.form['austim']
    if austim == 'yes':
        austim = 1
    else:
        austim = 0
    country_of_res = request.form['country_of_res']
    used_app_before = request.form['used_app_before']
    if used_app_before == 'yes':
        used_app_before = 1
    else:
        used_app_before = 0
    result = request.form['result']
    if result == 'yes':
        result == 1
    else:
        result == 0
    age_desc = request.form['age_desc']
    relation = request.form['relation']
    if request.method == 'POST':
       my_prediction = BernNB.predict([[float(A1_Score),float(A2_Score),float(A3_Score),float(A4_Score),float(A5_Score),float(A6_Score),float(A7_Score),float(A8_Score),float(A9_Score),float(A10_Score),float(age),float(gender),float(ethnicity),float(jaundice),float(austim),float(country_of_res),float(used_app_before),float(result),float(age_desc),float(relation)]])

       if 0 == my_prediction[0]:
           return render_template('nodisease.html')
       elif 1 == my_prediction[0] and int(age) < 18:
           return render_template('heartdisease.htm', stage=3, stage1=int(my_prediction[0]))
       elif 1 == my_prediction[0] and int(age) < 40:
           return render_template('heartdisease.htm', stage=2, stage1=int(my_prediction[0]))
       else:
           return render_template('heartdisease.htm', stage=int(my_prediction[0]))
    return render_template('user_account.html')
# ------------------------------------predict_page-----------------------------------------------------------------

# ------------------------------------search_page-----------------------------------------------------------------
@app.route('/search')
def search():
   return render_template('search.html')
# ------------------------------------search_page-----------------------------------------------------------------

# -------------------------------------user_register_page-------------------------------------------------------------------------

@ app.route('/user_register', methods=['POST', 'GET'])
def user_register():
   conn = sqlite3.connect('autism_database')
   cur = conn.cursor()
   if request.method == 'POST':
      name = request.form['uname']
      email = request.form['email']
      password = request.form['psw']
      gender = request.form['gender']
      age = request.form['age']

      cur.execute("insert into user(name,email,password,gender,age) values ('%s','%s','%s','%s','%s')" % (name, email, password, gender, age))
      conn.commit()
      # cur.close()
      print('data inserted')
      return redirect(url_for('user_login'))

   return render_template('user_register.html')
# -------------------------------------user_register_page-------------------------------------------------------------------------

# -------------------------------------user_account_page-------------------------------------------------------------------------
@app.route('/user_account',methods = ['POST', 'GET'])
def user_account():
   return render_template('user_account.html')
# -------------------------------------user_account_page-------------------------------------------------------------------------

# -------------------------------------user_logout_page-------------------------------------------------------------------------
@app.route("/logout")
def logout():
   session['logged_in'] = False
   return home()

@app.route("/logoutd",methods = ['POST','GET'])
def logoutd():
   return home()# -------------------------------------user_logout_page-------------------------------------------------------------------------

@app.route('/chatbot')
def chatbot():
   return render_template('index.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    response = str(english_bot.get_response(userText))

    appendfile=os.listdir('saved_conversations')[-1]
    appendfile= open('saved_conversations/'+str(filenumber),"a")
    appendfile.write('user : '+userText+'\n')
    appendfile.write('bot : '+response+'\n')
    appendfile.close()

    return response
if __name__ == '__main__':
   app.secret_key = os.urandom(12)
   app.run(debug=True)

