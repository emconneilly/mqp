from app import app
from flask import render_template, request, redirect
from app import ocsvmAPI as api
import os
import re
import sys

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


@app.route('/createModel', methods = ['POST'])
def createModel():
    error = ''
    training = request.files['trainFile']
    # Check that uploads folder exists
    if not(os.path.isdir('uploads/')):
        os.mkdir('uploads/')
    # Save the file to uploads
    file_name = training.filename
    file_path = os.path.join('uploads/', file_name)
    training.save(file_path)
    # Create config
    kernel = request.form['kernel']
    if not kernel in ['rbf', 'linear', 'poly', 'sigmoid']:
        error += "<br>Your kernel is not one of the specified options."
    gamma = request.form['gamma']
    if gamma != 'scale':
        try:
            gamma_num = float(gamma)
            if gamma_num < 0 or gamma_num > 1:
                error += "<br>Your gamma is not in the range specified."
        except Exception:
            error += "<br>Your gamma is not a number."
    nu = request.form['nu']
    try:
        nu_num = float(nu)
        if nu_num < 0 or nu_num > 1:
            error += "<br>Your nu is not in the range specified."
    except Exception:
        error += "<br>Your nu is not a number."
    # Check and prep file
    if api.fileMalformed(file_path):
        error+="<br>Training file was malformed."
    train, numSequences = api.prepFile(file_path)
    config = api.createConfig(kernel, gamma, nu)
    # Train Model
    if len(error)==0:
        model = api.train(train, config)
    # Create lists for test results
    results = []
    # Check if testing or predicting
    if (len(error)==0) and ('self' in request.form or 'consensus' in request.form or 'mixNES' in request.form or 'mixWithRandom' in request.form or 'mixAll' in request.form or 'custom' in request.form):
        # Perform Tests Requested
        if 'self' in request.form:
            accuracy, falsePos, falseNeg, truePos, trueNeg = api.testSelfWeb(model, train, numSequences, file_path)
            testType = "self"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
        if 'consensus' in request.form:
            consensus, numSequences = api.prepFile(resource_path('app/static/consensusTest.csv'))
            accuracy, falsePos, falseNeg, truePos, trueNeg = api.testData(model, consensus, resource_path('app/static/consensusTestLabels.csv'), resource_path('app/static/consensusTest.csv'))
            testType = "consensus"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
        if 'mixNES' in request.form:
            mixNES, numSequences = api.prepFile(resource_path('app/static/mixNESTest.csv'))
            accuracy, falsePos, falseNeg, truePos, trueNeg  = api.testData(model, mixNES, resource_path('app/static/mixNESTestLabels.csv'), resource_path('app/static/mixNESTest.csv'))
            testType = "mixNES"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
        if 'mixWithRandom' in request.form:
            mixWithRandom, numSequences = api.prepFile(resource_path('app/static/mixWithRandomTest.csv'))
            accuracy, falsePos, falseNeg, truePos, trueNeg  = api.testData(model, mixWithRandom, resource_path('app/static/mixWithRandomTestLabels.csv'), resource_path('app/static/mixWithRandomTest.csv'))
            testType = "mixWithRandom"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
        if 'mixAll' in request.form:
            mixAll, numSequences = api.prepFile(resource_path('app/static/mixAllTest.csv'))
            accuracy, falsePos, falseNeg, truePos, trueNeg  = api.testData(model, mixAll, resource_path('app/static/mixAllTestLabels.csv'), resource_path('app/static/mixAllTest.csv'))
            testType = "mixAll"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
        if 'custom' in request.form:
            testFile = request.files['testFile']
            testLabels = request.files['testLabels']
            # Save custom input to uploads
            testFile_name = testFile.filename
            testLabels_name = testLabels.filename
            if testFile_name == '':
                error+="<br>You selected a custom test, but did not upload a test sequence file."
            if testLabels_name == '':
                error+="<br>You selected a custom test, but did not upload a test label file."
            if len(error)==0:
                testFile_path = os.path.join('uploads/', testFile_name)
                testFile.save(testFile_path)
                testLabels_name = testLabels.filename
                testLabels_path = os.path.join('uploads/', testLabels_name)
                testLabels.save(testLabels_path)
            else:
                return render_template('error.html', error=error)
            # Run test
            if api.fileMalformed(testFile_path):
                error+="<br>Custom sequence test file was malformed."
            else:
                custom, numSequences = api.prepFile(testFile_path)
                accuracy, falsePos, falseNeg, truePos, trueNeg  = api.testData(model, custom, testLabels_path, testFile_path)
                testType = "custom"
                result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
                results.append(result)

        return render_template('createModel.html', results=results)
    # If predicting, read in sequence and predict sequences
    inputSequence = request.form['predictSequence']
    if len(inputSequence)<10:
        error+="<br>Your prediction sequence is too short. Please input a sequence at least 10 amino acids."
    if re.search(r"[^acdefghiklmnpqrstvwy]+", inputSequence.lower()) != None:
        error+="<br>Your prediction sequence has characters that do not denote amino acids. It may be helpful to check for line breaks and other symbols."
    if len(error)==0:
        miniSequences = api.getSequencesFromString(request.form['predictSequence'])
        preppedPredict = api.prepText(miniSequences)
        functional = api.predict(model, preppedPredict, miniSequences)
        return render_template('prediction.html', functional=functional)
        
    return render_template('error.html', error=error)

@app.route('/static/<path:filename>')
def get_file(filename):
    return send_from_dirctory('static', filename)