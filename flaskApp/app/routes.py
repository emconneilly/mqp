from app import app
from flask import render_template, request, redirect
from app import ocsvmAPI as api
import os
import re

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/createModel', methods = ['POST'])
def createModel():
    error = ''
    training = request.files['trainFile']
    # Save the file to uploads
    file_name = training.filename
    file_path = os.path.join('uploads/', file_name)
    training.save(file_path)
    # Create config
    kernel = request.form['kernel']
    gamma = request.form['gamma']
    nu = request.form['nu']
    # Check and prep file
    if api.fileMalformed(file_path):
        error+="\nTraining file was malformed."
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
            consensus, numSequences = api.prepFile('app/static/consensusTest.csv')
            accuracy, falsePos, falseNeg, truePos, trueNeg = api.testData(model, consensus, 'app/static/consensusTestLabels.csv', 'app/static/consensusTest.csv')
            testType = "consensus"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
        if 'mixNES' in request.form:
            mixNES, numSequences = api.prepFile('app/static/mixNESTest.csv')
            accuracy, falsePos, falseNeg, truePos, trueNeg  = api.testData(model, mixNES, 'app/static/mixNESTestLabels.csv', 'app/static/mixNESTest.csv')
            testType = "mixNES"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
        if 'mixWithRandom' in request.form:
            mixWithRandom, numSequences = api.prepFile('app/static/mixWithRandomTest.csv')
            accuracy, falsePos, falseNeg, truePos, trueNeg  = api.testData(model, mixWithRandom, 'app/static/mixWithRandomTestLabels.csv', 'app/static/mixWithRandomTest.csv')
            testType = "mixWithRandom"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
        if 'mixAll' in request.form:
            mixAll, numSequences = api.prepFile('app/static/mixAllTest.csv')
            accuracy, falsePos, falseNeg, truePos, trueNeg  = api.testData(model, mixAll, 'app/static/mixAllTestLabels.csv', 'app/static/mixAllTest.csv')
            testType = "mixAll"
            result = {'accuracy':accuracy, 'falsePos':falsePos, 'falseNeg':falseNeg, 'truePos':truePos, 'trueNeg':trueNeg, 'testType':testType}
            results.append(result)
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
            if api.fileMalformed(testFile_path):
                error+="\nCustom sequence test file was malformed."
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
        error+="\nYour prediction sequence is too short. Please input a sequence at least 10 amino acids."
    if re.search(r"[^acdefghiklmnpqrstvwy]+", inputSequence.lower()) != None:
        error+="\nYour prediction sequence has characters that do not denote amino acids. It may be helpful to check for line breaks and other symbols."
    if len(error)==0:
        miniSequences = api.getSequencesFromString(request.form['predictSequence'])
        preppedPredict = api.prepText(miniSequences)
        functional = api.predict(model, preppedPredict, miniSequences)
        return render_template('prediction.html', functional=functional)
        
    return render_template('error.html', error=error)

@app.route('/static/<path:filename>')
def get_file(filename):
    return send_from_dirctory('static', filename)