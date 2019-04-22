from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Or set inline
mongo = PyMongo(app, uri="mongodb://localhost:27017/scrape_mars")

@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_facts = mongo.db.collection.find_one()
    # Return template from index.html, as well as the data
    return render_template("index.html", mars_facts=mars_facts)

@app.route("/scrape")
def index():
    # Scrape the scrape_mars file
    mars_facts = scrape_mars.scrape()

    # Insert data to MongoDB
    mongo.db.collection.update({}, mars_facts, upsert=True)
    # Return to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
