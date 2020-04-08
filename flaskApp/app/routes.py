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
    # Create config
    kernel = request.form['kernel']
    gamma = request.form['gamma']
    nu = request.form['nu']
    train, numSequences = api.prepFile(file_path)
    config = api.createConfig(kernel, gamma, nu)
    # Train Model
    model = api.train(train, config)
    # Perform Tests Requested
    if 'self' in request.form:
        summary = api.testSelfWeb(model, train, numSequences)
    if 'consensus' in request.form:
        consensus, numSequences = api.prepFile('app/static/consensusTest.csv')
        summary = api.testData(model, consensus, 'app/static/consensusTestLabels.csv')
    if 'mixNES' in request.form:
        mixNES, numSequences = api.prepFile('app/static/mixNESTest.csv')
        summary = api.testData(model, mixNES, 'app/static/mixNESTestLabels.csv')
    if 'mixWithRandom' in request.form:
        mixWithRandom, numSequences = api.prepFile('app/static/mixWithRandomTest.csv')
        summary = api.testData(model, mixWithRandom, 'app/static/mixWithRandomTestLabels.csv')
    if 'mixAll' in request.form:
        mixAll, numSequences = api.prepFile('app/static/mixAllTest.csv')
        summary = api.testData(model, mixAll, 'app/static/mixAllTestLabels.csv')
    if 'custom' in request.form:
        testFile = request.files['testFile']
        testLabels = request.files['testLabels']
        # Save custom input to uploads
        testFile_name = testFile.filename
        testFile_path = os.path.join('uploads/', testFile_name)
        testFile.save(testFile_path)
        testLabels_name = testLabels.filename
        testLabels_path = os.path.join('uploads/', testLabels_name)
        testLabels.save(testLabels_path)
        # Run test
        custom, numSequences = api.prepFile(testFile_path)
        summary = api.testData(model, custom, testLabels_path)
    
    return render_template('createModel.html', summary=summary)

@app.route('/static/<path:filename>')
def get_file(filename):
    return send_from_dirctory('static', filename)