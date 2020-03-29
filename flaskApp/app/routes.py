from app import app
from flask import render_template, request, redirect
from app import ocsvmAPI as api
import os

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/createModel', methods = ['POST'])
def createModel():
    training = request.files['trainFile']
    # Save the file to uploads
    file_name = training.filename
    file_path = os.path.join('uploads/', file_name)
    training.save(file_path)
    
    kernel = request.form['kernel']
    gamma = request.form['gamma']
    nu = request.form['nu']
    train, numSequences = api.prepFile(file_path)
    config = api.createConfig(kernel, gamma, nu)
    model = api.train(train, config)
    summary = api.testSelfWeb(model, train, numSequences)
    return render_template('createModel.html', summary=summary)

@app.route('/static/<path:filename>')
def get_file(filename):
    return send_from_dirctory('static', filename)