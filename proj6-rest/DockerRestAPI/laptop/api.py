# Laptop Service
from flask import Flask
import flask
from flask import request
from pymongo import MongoClient
import pymongo
from flask_restful import Resource, Api
import os

# Instantiate the app
app = Flask(__name__)
api = Api(app)

#from docker-compose.yml
client = MongoClient("db", 27017)
db = client.tododb

#all values, in json by default
class allL(Resource):
    def get(self):

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
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))

        return {
            'openTime': [item['openInfoDone'] for item in _items]
        }

class openJson(Resource):
    def get(self):
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("openTime", pymongo.ASCENDING).limit(int(top))
        
        return {
            'openTime': [item['openInfoDone'] for item in _items]
        }

class openCSV(Resource):
    def get(self):
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
        top = request.args.get("top")
        if (top == None): top = 20

        #sort by closeTime now
        _items = db.tododb.find().sort("closeTime", pymongo.ASCENDING).limit(int(top))

        return {
            'closeTime': [item['closeInfoDone'] for item in _items]
        }

class closeJson(Resource):
    def get(self):
        top = request.args.get("top")
        if (top == None): top = 20

        _items = db.tododb.find().sort("closeTime", pymongo.ASCENDING).limit(int(top))

        return {
            'closeTime': [item['closeInfoDone'] for item in _items]
        }

class closeCSV(Resource):
    def get(self):
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
