# Runnable Tool that takes prompts the user for input to train and test an OC SVM Model

import ocsvmAPI as api 
import sys

#Get data
print('Welcome to the NES Model Training Tool! To train and test the model, please follow along.')
print('To use your own dataset, please make sure it is in csv format with one sequence on each line.')
print('Input the name of the training dataset: ')
trainRaw = input()

#Prep data
train = api.prepFile(trainRaw)

#Explain parameters
print("This model requires some parameters to be set. These include a kernel, gamma, and nu.")
print("Would you like these to be explained in more detail? (y/n)")
explain = input()
if explain == 'y':
    print("The kernel is the function the model will use to transform the data if it needs to be fit in a higher dimension.")
    print("When the data does not need to be fit in a higher dimension, a linear kernel will fit the data as is.\n")
    print("Gamma is a representation of the impact of each training value on the model's fit.")
    print("A higher gamma means each value has less influence and a lower gamma means each value has more influence.\n")
    print("Nu is the upper bound of the proportion of training values that the model can label as an incorrect group.\n")

#Get parameters
print("Some parameters have been chosen through iterative testing as defaults.")
print('What would you like to set as the kernel? (default = rbf) ')
print("The options are linear, poly, rbf, or sigmoid")
kernel = input()
print('What would you like to use for gamma? (default = 1/number of features)')
print("It should be a number in the range (0,1]")
gamma = input()
print('What would you like to use for nu? (default = 0.2)')
print("It must be a number in the range (0,1]")
nu = input()
config = api.createConfig(kernel, gamma, nu)

#Train model
model = api.train(train, config)

#Get testing instructions
choice = ''
fname = ''
print('It is time to test the model!')
while choice != 'exit':
    print('\n\nYou can test as many times as you would like. To end the session with this model, input "exit"')
    print('If you would like to save your test runs, enter "save". Save capture tests until you select "stop save".')
    print('Testing options:')
    print('test on the training data: self')
    print('test on a strictly literature consensus set: consensus')
    print('test on a mix of consensus and nonconsesnus NES: mixNES')
    print('test on a mix of consensus NES and random sequences: mixWithRandom')
    print('test on a mix of consensus NES, nonconsesnus NES, and random sequences: mixAll')
    print('test on all of the pre-loaded data: all')
    print('test on custom data: custom\n')

    #Test model
    choice = input()
    if choice == 'save':
        print('Please enter a name for the save file that you will recognize later (without the extension):')
        fname = input()
        saved = open(fname + '.txt', "w")
        saved.close()
    elif choice == 'stop save':
        fname = ''
    elif choice == 'self':
        print('\nInput the name of the label file for the training dataset: ')
        labelFile = input()
        print('\n--Testing against self--')
        api.testData(model, train, labelFile)
        if fname != '':
            api.testDataSave(model, train, labelFile, fname, 'Self')
    elif choice == 'consensus':
        print('\n--Testing against consensus--')
        api.testData(model, api.prepFile('consensusTest.csv'), 'consensusTestLabels.csv')
        if fname != '':
            api.testDataSave(model, api.prepFile('consensusTest.csv'), 'consensusTestLabels.csv', fname, 'Consensus')
    elif choice == 'mixNES':
        print('\n--Testing against mixNES--')
        api.testData(model, api.prepFile('mixNESTest.csv'), 'mixNESTestLabels.csv')
        if fname != '':
            api.testDataSave(model, api.prepFile('mixNESTest.csv'), 'mixNESTestLabels.csv', fname, 'MixNES')
    elif choice == 'mixWithRandom':
        print('\n--Testing against mixWithRandom--')
        api.testData(model, api.prepFile('mixWithRandomTest.csv'), 'mixWithRandomTestLabels.csv')
        if fname != '':
            api.testDataSave(model, api.prepFile('mixWithRandomTest.csv'), 'mixWithRandomTestLabels.csv', fname, 'MixWithRandom')
    elif choice == 'mixAll':
        print('\n--Testing against mixAll--')
        api.testData(model, api.prepFile('mixAllTest.csv'), 'mixAllTestLabels.csv')
        if fname != '':
            api.testDataSave(model, api.prepFile('mixAllTest.csv'), 'mixAllTestLabels.csv', fname, 'MixAll')
    elif choice == 'all':
        print('\nInput the name of the label file for the training dataset: ')
        labelFile = input()
        print('\n--Testing against self--')
        api.testData(model, train, labelFile)
        print('\n--Testing against consensus--')
        api.testData(model, api.prepFile('consensusTest.csv'), 'consensusTestLabels.csv')
        print('\n--Testing against mixNES--')
        api.testData(model, api.prepFile('mixNESTest.csv'), 'mixNESTestLabels.csv')
        print('\n--Testing against mixWithRandom--')
        api.testData(model, api.prepFile('mixWithRandomTest.csv'), 'mixWithRandomTestLabels.csv')
        print('\n--Testing against mixAll--')
        api.testData(model, api.prepFile('mixAllTest.csv'), 'mixAllTestLabels.csv')
        if fname != '':
            api.testDataSave(model, train, labelFile, fname, 'Self')
            api.testDataSave(model, api.prepFile('consensusTest.csv'), 'consensusTestLabels.csv', fname, 'Consensus')
            api.testDataSave(model, api.prepFile('mixNESTest.csv'), 'mixNESTestLabels.csv', fname, 'MixNES')
            api.testDataSave(model, api.prepFile('mixWithRandomTest.csv'), 'mixWithRandomTestLabels.csv', fname, 'MixWithRandom')
            api.testDataSave(model, api.prepFile('mixAllTest.csv'), 'mixAllTestLabels.csv', fname, 'MixAll')
    elif choice == 'custom':
        print('\nInput the name of the test dataset: ')
        testData = input()
        print('Input the name of the label file for the test dataset: ')
        testLabel = input()
        print('\n--Testing against custom--')
        api.testData(model, api.prepFile(testData), testLabel)
        if fname != '':
            api.testDataSave(model, api.prepFile(testData), testLabel, fname, 'Custom')
    elif choice != 'exit':
        print('Sorry, that was not a valid option')
api.sys.exit()