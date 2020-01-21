#!/usr/bin/python3
"""
Write a script that starts a Flask web application:
"""

from flask import Flask, render_template
from models import storage
app = Flask(__name__)
strict_slashes = False


@app.route("/")
def hello():
    """ root routing """
    return "Hello HBNB!"


@app.route("/hbnb")
def hello1():
    """ extension hbnb """
    return "HBNB"


@app.route("/c/<arg>")
def hello2(arg):
    """ extension c/text """
    string = "C " + arg
    return string.replace("_", " ")


@app.route("/python/")
@app.route("/python")
def hello3():
    """ extension /python """
    return "Python is cool"


@app.route("/python/<arg>")
def hello3a(arg):
    """ extension python/text """
    string = "Python " + arg
    return string.replace("_", " ")


@app.route("/number/<int:num>")
def hello4(num):
    """ extension number/<num> """

    return str(num) + " is a number"


@app.route("/number_template/<int:num>")
def hello5(num):
    return render_template('5-number.html', number=num)


@app.route("/number_odd_or_even/<int:num>")
def hello6(num):
    word = "even"
    if num % 2:
        word = "odd"
    return render_template('6-number_odd_or_even.html',
                           number=num, string=word)


@app.teardown_appcontext
def teardown_DB(response_or_exec):
    """ tears down the db """
    storage.close()


@app.route("/states_list")
def hello7():
    """ returning states """
    statesArr = list(storage.all("State").values())
    statesArr.sort(key=lambda statesArr: statesArr.name)
    return render_template('7-states_list.html', states=statesArr)


@app.route("/cities_by_states")
def hello8():
    """ returning cities by states """
    statesArr = list(storage.all("State").values())
    statesArr.sort(key=lambda statesArr: statesArr.name)
    for state in statesArr:
        state.cities.sort(key=lambda statesArr: statesArr.name)
    return render_template('8-cities_by_states.html', states=statesArr)


@app.route("/states")
def hello9half():
    """ if no id passed """
    statesArr = list(storage.all("State").values())
    statesArr.sort(key=lambda statesArr: statesArr.name)
    return render_template("9-states.html", states=statesArr, state_id=None)


@app.route("/states/<state_id>")
def hello9(state_id=None):
    """ sets up the cities in states """
    statesArr = storage.all("State")
    if state_id:
        state = statesArr.get("State.{}".format(state_id))
        if state:
            statesArr = [state]
        else:
            statesArr = []
    else:
        statesArr = list(statesArr.values())

    statesArr.sort(key=lambda statesArr: statesArr.name)
    for state in statesArr:
        state.cities.sort(key=lambda statesArr: statesArr.name)
    return render_template(
        "9-states.html", states=statesArr, state_id=state_id)


@app.route("/hbnb_filters")
def hello10():
    """ sets up the cities in states """
    stateArray = list(storage.all("State").values())
    stateArray.sort(key=lambda array: array.name)
    for state in stateArray:
        state.cities.sort(key=lambda array: array.name)
    amenities = list(storage.all("Amenity").values())
    amenities.sort(key=lambda array: array.name)
    return render_template(
            "10-hbnb_filters.html",
            state=stateArray, amenities=amenities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
