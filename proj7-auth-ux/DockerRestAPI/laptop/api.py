# Laptop Service
from flask import Flask, request, session
import flask
from flask import request
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
import pymongo
from flask_restful import Resource, Api
import os
from random import randint
from wtforms import Form, BooleanField, StringField, validators, PasswordField
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)
import time
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import (LoginManager, current_user, login_required,
                            login_user, logout_user, UserMixin, 
                            confirm_login, fresh_login_required)

# Instantiate the app
app = Flask(__name__)
#csrf = CSRFProtect(app)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ('/api/login')

app.config['SECRET_KEY'] = "yeah, not actually a secret"


#from docker-compose.yml
client = MongoClient("db", 27017)
db = client.tododb
users = db.userdb
#csrf_token = 'asdhfklh'


#our register and login forms that coincide with register and login html files
class RegisterForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(message=u'Enter username')])
    password = StringField('Password', validators=[validators.DataRequired(message=u'Enter password')])
    
class LoginForm(Form):
    username = StringField('Username', validators=[validators.DataRequired(message=u'Enter username')])
    password = StringField('Password', validators=[validators.DataRequired(message=u'Enter password')])
    remember = BooleanField('Remember Me')

#user class to get our IDs    
class UserInfo(UserMixin):
    def __init__(self, user_id):
        self.id = str(user_id)


@app.route("/api/register", methods=["GET", "POST"])
def register():

    #get user input from registration forms
    form = RegisterForm(request.form)
    username = form.username.data
    password = form.password.data
    
    makeId = "" 

    #take action once user has submitted
    if form.validate():
        #get username in database
        item = db.tododb.find_one({"username":username})
        #make our random id for username
        makeId = randint(1,50000)

        #if user/pass not found, return 400 error
        if (username == None) or (password == None):
            return 'no username or password given', 400
        if item != None:
            return 'try a different username', 400

        #hash the password
        hVal = hash_password(password)

        #add our new user with its info into our users database
        new = {"_id": makeId, 'username': username, 'password': hVal}
        users.insert_one(new)

        #push this result out from above in json format
        result = {'location': makeId, 'username': username, 'password': hVal}
        
        return flask.jsonify(result=result), 201

    #back to register if never submitted or got here from error
    return flask.render_template('register.html', form=form)

#loads and returns the user and its ID
@login_manager.user_loader
def load_user(user_id):
    userInfo = users.find({"_id": int(user_id)})
    if (userInfo == None): return None
    return UserInfo(user_id)

#encrypts password so its not the say 10 characters user entered
def hash_password(password):
    return pwd_context.encrypt(password)

#checks if password matches on login
def verify_password(password, hashVal):
    return pwd_context.verify(password, hashVal)

#generate our token
def generate_auth_token(user_id, expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    # pass index of user
    token = s.dumps({'id': user_id})
    return {'token': token, 'duration': expiration}

#verify our token
def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None    # valid token, but expired
    except BadSignature:
        return None    # invalid token
    return "Success"

@app.route("/api/login", methods=["GET", "POST"])
def login():
    #get our form and its values
    form = LoginForm(request.form)
    if (request.method == "POST") and (form.validate()):
        username = form.username.data
        password = form.password.data
        rememberl = form.remember.data
        #get our user info from userclass
        userInfo = users.find({"username":username})

        #if we index userInfo and get IndexError, that means
        #that there is no such user. so we take them back to the
        #register page
        try:
            userInfo[0]
        except IndexError:
            return redirect(url_for("register"))
        
        #get our password from userInfo and make sure its right for the user   
        entry = userInfo[0]
        hVal = entry['password']
        if verify_password(password, hVal) is True:

            #now get the username ID and create an active session
            #entryTwo=userInfo[0]
            actID = entry['_id']
            session['user_id'] = actID
            user = UserInfo(actID)
            
            #log the user in
            login_user(user, remember = rememberl)
            return redirect(request.args.get("next") or url_for("token"))

        #if they ran into an issue and they get here, they'll be sent back to register
        else: return redirect(url_for("register"))

    #login page          
    return flask.render_template('login.html', form=form)

#logout the user and send them back to the index page to choose from options
@app.route("/api/logout")
@login_required
def logout():
    logout_user()
    return "You've been Logged out"

#index page with login, logout, and register
@app.route("/")
def index():
    return flask.render_template("index.html")

#sets up our token               
@app.route("/api/token", methods=['GET'])
@login_required
def token():
    #get user_id from login session
    user_id = session.get('user_id')
    #generate a token to tie to the user
    tokenInfo = generate_auth_token(user_id, 600)
    #get token in proper form
    retToken = tokenInfo['token']
    retToken = retToken.decode('utf-8')
    
    #now return the token and the duration in json
    result = {'token': retToken, 'duration': 60}
    return flask.jsonify(result=result)

#all values, in json by default
class allL(Resource):
    def get(self):

        #get the token the user put in the url, and verify its the right one
        #respond appropriately if not
        #do this for all the APIs
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401

        #checks the URL and grabs any top value user may have entered (i.e. top = 3)
        top = request.args.get("top")

        #if user didn't give us any top, then we are just going to display 20 values
        #as stated in the default size from calc.html
        if (top == None): top = 20

        #grab the items the user inputed
        #in the case the user submitted a top value, we want to be in ascending order
        #as stated in the README when there are top values. So pymongo function
        #ASCENDING will accomplish this
        #limit the values by user entered top or by 20
        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        #set up our list / unpack it some
        items = [item for item in _items]

       #collect open and close times from _items and our variables in new() from app.py
        return {
            'openTime': [item['openInfoDone'] for item in items],
            'closeTime': [item['closeInfoDone'] for item in items]
        }

#all values in json...and so on for the others
class allJson(Resource):
    def get(self):
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401
        
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))
        items = [item for item in _items]
   
        return {
            'openTime': [item['openInfoDone'] for item in items],
            'closeTime': [item['closeInfoDone'] for item in items]
        }

class allCSV(Resource):
    def get(self):
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401
        
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))
        items = [item for item in _items]

        #split each value up by a comma and loop through the list and add
        csv = ""
        for item in items:
            csv += item['openInfoDone'] + ', ' + item['closeInfoDone'] + ', '

        return csv

class openL(Resource):
    def get(self):
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401
        
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        return {
            'openTime': [item['openInfoDone'] for item in _items]
        }

class openJson(Resource):
    def get(self):
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401
        
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))
        
        return {
            'openTime': [item['openInfoDone'] for item in _items]
        }

class openCSV(Resource):
    def get(self):
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401
        
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))
        items = [item for item in _items]

        csv = ""
        for item in items:
            csv += item['openInfoDone'] + ', '
        return csv

class closeL(Resource):
    def get(self):
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401
        
        top = request.args.get("top")
        if (top == None): top = 20

        #sort by closeTime now
        _items = db.tododb.find().sort("closeTime", pymongo.ASCENDING).limit(int(top))

        return {
            'closeTime': [item['closeInfoDone'] for item in _items]
        }

class closeJson(Resource):
    def get(self):
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401
        
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("closeTime", pymongo.ASCENDING).limit(int(top))

        return {
            'closeTime': [item['closeInfoDone'] for item in _items]
        }

class closeCSV(Resource):
    def get(self):
        token = request.args.get('token')
        if token == None: return 'please enter a token value in your link', 401
        verify = verify_auth_token(token)
        if verify == None: return 'token could not be verified', 401
        
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("closeTime", pymongo.ASCENDING).limit(int(top))
        items = [item for item in _items]


        csv = ""
        for item in items:
            csv += item['closeInfoDone'] + ', '
        return csv

# Create routes
# Another way, without decorators
#api.add_resource(Laptop, '/')

api.add_resource(allL, '/listAll')
api.add_resource(allJson, '/listAll/json')
api.add_resource(allCSV, '/listAll/csv')

api.add_resource(openL, '/listOpenOnly')
api.add_resource(openJson, '/listOpenOnly/json')
api.add_resource(openCSV, '/listOpenOnly/csv')

api.add_resource(closeL, '/listCloseOnly')
api.add_resource(closeJson, '/listCloseOnly/json')
api.add_resource(closeCSV, '/listCloseOnly/csv')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
