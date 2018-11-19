from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars = mongo.db.scraped_data.find_one()

    # Return template and data
    return render_template("index.html", mars=mars)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = scrape_mars.scrape_data()

    if mars_data != 'err':
        # Update the Mongo database using update and upsert=True
        mongo.db.scraped_data.update({}, mars_data, upsert=True)
    else:
        mars_data = scrape_mars.scrape_data()
        try:
            # Update the Mongo database using update and upsert=True
            mongo.db.scraped_data.update({}, mars_data, upsert=True)
        except:
            print('scrape_data() function failed 2x.')

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
