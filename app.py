import pandas as pd
import csv
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)


app = Flask(__name__)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/precipitation<br/>"
        f"/api/stations<br/>"
        f"/api/temperature<br/>"
        f"/api/<start><br/>"
        f"/api/<start>/<end>"
    )


@app.route("/api/precipitation")
def precipitation():
    """all the precipitation values"""
    result = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > "2016-08-22").all()
    all_dates = []
    for date, prcp in result:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_dates.append(prcp_dict)

    return jsonify(all_dates)


@app.route("/api/stations")
def stations():
    """all the stations"""
    result = session.query(Station.name).all()
    all_stations = list(np.ravel(result))
    return jsonify(all_stations)


@app.route("/api/temperature")
def temperature():
    """all the temperature values a year from last data point"""
    result = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > "2016-08-22").all()
    all_temp = []
    for date, tobs in result:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temperature"] = tobs
        all_temp.append(temp_dict)
    return jsonify(all_temp)


@app.route("/api/<start>/<end>")
def api(start, end=0):
    """"minimum, maximum and average temperature for a date range"""

    result = session.query(func.min(Measurement.tobs),
                           func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    all_result = list(np.ravel(result))
    return jsonify(all_result)


if __name__ == "__main__":
    app.run(debug=True)
