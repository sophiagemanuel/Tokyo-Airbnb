# Import the dependencies.
import warnings
warnings.filterwarnings('ignore')

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import numpy as np

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/tokyoAirbnb.sqlite")

# reflect an existing database into a new model

Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True, schema='main')


# Create our session (link) from Python to the DB
session = Session(engine)


# Save references to each table

tokyo_airbnb = Base.classes.tokyoAirbnb

# #################################################
# # Flask Setup
# #################################################

from flask import Flask, jsonify

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return(
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/neighbourhoods<br/>")

@app.route("/api/v1.0/neighbourhoods")
def neighbourhoods():

    neighbourhoods = session.query(tokyo_airbnb.neighbourhood).all()

    all_neighbourhoods = list(np.ravel(neighbourhoods))
    
    return jsonify(all_neighbourhoods)


if __name__ == "__main__":
    app.run(debug=True)

session.close()
