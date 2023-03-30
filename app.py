##Importing Packages
from flask import Flask,render_template,request,redirect,url_for,session,flash
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pylab import rcParams
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import tweepy
import preprocessor as p
from transformers import pipeline

##App Definition
app = Flask(__name__)
app.secret_key = 'Muthu_Palaniappan_M_211101079'

##Twitter App Config
consumer_key = '---------------------'
consumer_secret = '----------------------'
access_token = '------------------'
access_token_secret = '----------------------'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

##MySQL Database Config
app.config['MYSQL_HOST'] = '--------------'
app.config['MYSQL_USER'] = '---------'
app.config['MYSQL_PASSWORD'] = '--------'
app.config['MYSQL_DB'] = '------------'
mysql = MySQL(app)

##Ploting Config
rcParams['figure.figsize'] = 10,5

## Define pipeline outside of the route function for performance reasons
ZSL = pipeline("zero-shot-classification")

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/login',methods = ['GET','POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from users_signin where email = %s and password = %s',(email,password))
        us_acc = cursor.fetchone()

        if us_acc:
            session['loggedin'] = True
            session['id'] = us_acc['email']
            session['username'] = us_acc['email']
            msg = "Log In Sucessfull"
            print(msg)
            return render_template('form.html')
        else:
            msg = 'Incorrect username / password !'
            return render_template('index.html')
            print(msg)

    return render_template('index.html')

@app.route('/register',methods = ['GET','POST'])
def register():
    msg = ""
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form and 'Name' in request.form:
        Name = request.form['Name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users_signin WHERE email = % s', (email, ))
        us_acc = cursor.fetchone()
        print(Name,email)

        if us_acc:

            msg = 'Account already exists !'
            flash('This email is already registered. Please use a different email.')

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):

            msg = 'Invalid email address !'

        elif not re.match(r'[A-Za-z0-9]+', Name):

            msg = 'Username must contain only characters and numbers !'

        elif not Name or not password or not email:

            msg = 'Please fill out the form !'
        
        else:
            cursor.execute('insert into users_signin values (%s,%s,%s)',(email,password,Name))
            mysql.connection.commit()
            msg = 'Registration Sucessfull!!!'
    print(msg)
    return render_template('index.html')

@app.route('/pred', methods=['GET', 'POST'])
def pred():
    if request.method == 'POST':
        # Get form data
        tw_link = request.form['tw_id']
        label = []
        for i in range(1,4):
            label.append(request.form[f'Label{i}'])
        
        ##Extracting the Tweet ID from the twitter Link
        t_id = re.search("(?<=status\/).*",tw_link)
        if t_id:
            t_id = t_id.group(0)
            tweet_id = api.get_status(t_id).id
            tweet = api.get_status(tweet_id)
            username = tweet.user.screen_name
            tweet_text_1 = tweet.text
            tweet_text = p.clean(tweet_text_1)
        else:
            print("Bad Request - Client Side")

        # Run zero-shot classification
        result_labels = ZSL(sequences=tweet_text, candidate_labels=label, multi_class=True)
        labels = result_labels['labels']
        scores = result_labels['scores']

        # Set color palette
        color_palette = ['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854']

        # Create bar chart of label probabilities
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.bar(labels, scores, color=color_palette)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(top=False, right=False)
        ax.set_xticklabels(labels, rotation=90, fontsize=12)
        ax.set_xlabel('Label', fontsize=14)
        ax.set_ylabel('Probability', fontsize=14)
        ax.set_ylim([0, 1])
        ax.yaxis.grid(True, linestyle='--', linewidth=0.5)
        plt.tight_layout()

        # Save plot
        new_plot_name = "plot" +str(time.time()) +".png"
        for filename in os.listdir('../TweetTagNavigator/static/'):
            if filename.startswith('plot'):
                os.remove('../TweetTagNavigator/static/'+filename)
        plt.savefig('../TweetTagNavigator/static/'+new_plot_name)

        
        # Render template with results
        return render_template('result.html', labels=labels, scores=scores,graph=new_plot_name,user_name=username,Tweet_=tweet_text_1)
    
    # Render form template on GET request
    return render_template('form.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
