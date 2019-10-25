from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/nasamars_app"
# config document which is gon be a dictionary
mongo = PyMongo(app)




@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html",mars=mars)
# get the data from the database and put it into the template

@app.route("/scrape")
def scraper():
    mars= mongo.db.mars
    # get the scrape func from "scrape_mars"
    mars_data = scrape_mars.scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
