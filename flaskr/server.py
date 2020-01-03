from flask import Flask,render_template
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import json

server = Flask(__name__)

@server.route('/')
def index():
    return render_template('index.html',page='baidu')

from flaskr.route import baidu
server.register_blueprint(baidu.bp)


