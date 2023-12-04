# Import the dependencies.
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table

Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (f"Welcome to my Module 10 Challenge SQL Alchemy page!<br/>"
            f"Available Routes: <br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/station<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end>"
            )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Precipitation Analysis
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_ago

# Perform a query to retrieve the data and precipitation scores


    y_prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_ago).\
        order_by(Measurement.date)
  

    session.close()


    all_y_prcp = []
    for date, precipitation in y_prcp:
        y_prcp_dict = {}
        y_prcp_dict["date"] = date
        y_prcp_dict["precipitation"] = precipitation
        all_y_prcp.append(y_prcp_dict)

    return jsonify(all_y_prcp)

#Return a JSON list of stations from the dataset



@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    count = func.count(Measurement.station)
    sel = [Measurement.station,
        count]
    active_station = session.query(*sel).\
        group_by(Measurement.station).\
        order_by(count.desc()).all()
    active_station
  
    session.close()

    active_station_list = []
    for station in active_station:
        active_station_dict = {}
        active_station_dict["station"] = station.station
        active_station_list.append(active_station_dict)
      
    return jsonify(active_station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    year_ago


    y_tobs = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= year_ago).\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.tobs)

    session.close()


    most_active_station = []
    for station, date,tobs in y_tobs:
        most_active_dict = {}
        most_active_dict['station'] = station
        most_active_dict['date'] = date
        most_active_dict['tobs'] = tobs
        most_active_station.append(most_active_dict)
      
    return jsonify(most_active_station)


# @app.route("/api/v1.0/<start>")
# def (start):
   

#     canonicalized = datetime.strptime(start, "%y-%m-%d").date()
#     for date in Measurement:
#         search_term = date["date"]

#         if search_term == canonicalized:
#             return jsonify(date)

#     return jsonify({"error": f"Character with real_name {date} not found."}), 404




# @app.route("/api/v1.0/<start>/<end>")
# def <start>/<end>():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

if __name__ == "__main__":
    app.run(debug=True)

