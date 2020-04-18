from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os


app = Flask(__name__)


mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars")


@app.route('/')
def index():
    first_data = mongo.db.mission_to_mars.find_one()
    print(first_data)
    return render_template('index.html', mission_to_mars=first_data)


@app.route('/scrape')
def scrape():
    target_collection = mongo.db.mission_to_mars
    update_data = scrape_mars.scrape()
    target_collection.update(
        {},
        update_data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)

# from flask import Flask, jsonify
# import scrape_mars

# #################################################
# # Flask Setup
# #################################################
# app = Flask(__name__)


# #################################################
# # Flask Routes
# #################################################

# @app.route("/")
# def welcome():
#     """List all available api routes."""
#     return "Mission to Mars"


# @app.route("/scrape")
# def names():
#     data = scrape_mars.scrape()
#     return data


# if __name__ == '__main__':
#     app.run(debug=True)