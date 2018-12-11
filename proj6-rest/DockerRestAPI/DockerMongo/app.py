import os
import flask
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

app = Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

client = MongoClient("db", 27017)
db = client.tododb
db.tododb.delete_many({}) #deletes old data storage if program is reset

#index route from flask_brevets
@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

#errorhandler from flask_brevets
@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    #select brevet distance, this is our distance box that we will
    #get user input from
    #we will see the below again in the getJSON call in calc.html
    distance = request.args.get('distance', 999, type = int)

    if (km < 0): km = 0 #get rid of any negatives and just set it to 0 for the person

    #get start date and time, and then combine with arrow into one date/moment
    #these are our boxes for date and time on host page
    #similar to getting km except string instead of float
    sdate = request.args.get('sdate', "", type = str)
    stime = request.args.get('stime', "", type = str)
    starting_time = arrow.get(sdate + " " + stime, 'YYYY-MM-DD HH:mm')
    starting_time = starting_time.isoformat()

    
    # FIXME: These probably aren't the right open and close times
    # and brevets may be longer than 200km
    #we can now replace (arrow.now().isoformat) with starting_time as we are able
    #to collect the starting/initial time from the user. Same goes for 200, can
    #be replaced with "distance" aka user input
    open_time = acp_times.open_time(km, distance, starting_time)
    close_time = acp_times.close_time(km, distance, starting_time)
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


##@app.route('/')
##def todo():
####    _items = db.tododb.find()
####    items = [item for item in _items]
####
####    return render_template('todo.html', items=items)
####   return render_template('calc.html')


@app.route('/display', methods=['POST'])
def display():
    #checkpoint, opentime, closetime stored
    _items = db.tododb.find()
    items = [item for item in _items]

    #if there are no values entered then nothing to display
    #return warning message
    if (len(items) == 0): return render_template('errorWarning.html')

    #else, go to html and display checkpoint, opentime, closetime
    return render_template('display.html', items=items)

#if the user hits submit with no values entered, then go here and
#show them the error
@app.route('/submiterror')
def submiterror():
    return render_template('submiterror.html')
    

@app.route('/new', methods=['POST'])
def new():
    
    #get the values the user entered/program displayed
    openInfo = request.form.getlist("open")
    closeInfo = request.form.getlist("close")
    kmInfo = request.form.getlist("km")

    #our lists to store opentime(siftedO) closetime(siftedC)
    #and km(siftedK)
    siftedO = []
    siftedC = []
    siftedK = []

    #if the value isn't empty, then add it into the list
    for item in openInfo:
        if (str(item) != ""): siftedO.append(str(item))

    for item in closeInfo:
        if (str(item) != ""): siftedC.append(str(item))

    for item in kmInfo:
        if (str(item) != ""): siftedK.append(str(item))

    #take the longest length list if for some reason
    #one got bigger than the other. This length will
    #iterate and print out for the longest list so as
    #to make sure nothing gets left behind
    length = max(len(siftedO), len(siftedC), len(siftedK))

    #if theres nothing in any list, and the user tries to
    #hit submit, then we'll give them an error
    if length == 0:
        return redirect(url_for('submiterror'))

    #go through the lists assign item values. These will be
    #printed out in display HTML later on. Previously from the
    #start app.py def new() method
    for i in range(length):
        item_doc = {
            'openInfoDone': siftedO[i],
            'closeInfoDone': siftedC[i],
            'kmInfoDone': siftedK[i]
        }
        db.tododb.insert_one(item_doc)

    #once we are done with the set of values the user submitted, head back
    #to index (and thus main calc page) and do it again at home page
    return redirect(url_for('index'))

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
