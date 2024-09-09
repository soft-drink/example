#!/usr/bin/env python3
# $ flask --app main run

from flask import Flask, request, Response
import matplotlib.pyplot as plt

import io
from math import sin, cos
from time import time


app = Flask(__name__)


@app.route("/plot.png")
def plot():
    def plot_func(x, coeff1 = 1, coeff2 = 1):
        return sin(coeff1 * x) + cos(coeff2 * x)

    BEGIN = time()
    COUNT = 5000
    SCALE = 25

    axis_x, axis_y = [], []
    buffer = io.BytesIO()
    arg = request.args

    try:
        a = float(arg.get("a", "1"))
    except:
        a = 1
    try:
        b = float(arg.get("b", "1"))
    except:
        b = 1

    for i in range(COUNT):
        x = SCALE * i / COUNT
        y = plot_func(x, a, b)
        axis_x.append(x)
        axis_y.append(y)
    plt.figure()
    plt.plot(axis_x, axis_y)

    fig = plt.savefig(buffer)
    result = Response(buffer.getvalue(), mimetype = "image/png")
    END = time()
    print("%dms" % ((END - BEGIN) * 1000, ))
    return result

@app.route("/")
def landing_page():
    return '''
<html>
<head><title>Plot</title></head><body>
<img id="plot" height="400" width="400" src="plot.png" /><br />
<label for="axis_x">x:</label><input id="axis_x" type="number" with="250" value="1" />
<label for="axis_y">y:</label><input id="axis_y" type="number" with="250" value="1" />
<input type="button" height="50" width="150" value="OK" 
onclick="javascript:document.getElementById('plot').src='plot.png?a=' + document.getElementById('axis_x').value + '&b=' + document.getElementById('axis_y').value;"
/><br /></body>
'''

