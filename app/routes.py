from app import app, socket
from flask_socketio import emit
from flask import render_template, flash, redirect, url_for
from flask import request
import json
import os
import re
import time

from .models.sim import Sim

@app.route('/')
@app.route('/index')
def index():
    files = [f for f in os.listdir('./data') if re.match(r'.*\.json', f)]
    return render_template('index.html', files=files)

@app.route('/scenario/<file>')
def scenario(file):
    sim = Sim.loadfile(file)
    return render_template('scenario.html', sim=sim)

@socket.on('simulate')
def simulate(msg):
    file = msg.get("file","")
    print("simulate ", file)
    sim = Sim.loadfile(file)
    data = sim.export_data()
    emit('init',data)
    for i in range(sim.n):
        step = sim.step()
        time.sleep(0.01)
        emit('update',step)

