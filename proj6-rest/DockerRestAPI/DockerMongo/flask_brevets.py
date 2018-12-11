"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.secret_key = CONFIG.SECRET_KEY

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
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


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
