# Runnable Tool that takes prompts the user for input to train and test an OC SVM Model

import ocsvmAPI as api 

#Get data
print('Welcome to the NES Model Training Tool! To train and test the model, please follow along.')
print('Input the name of the training dataset: ')
trainRaw = input()

#Prep data
train = api.prepFile(trainRaw)

#Get parameters
print('Would you like to use the default parameters? (y/n) ')
default = input()
if default == 'n':
    print('What would you like to set as the kernel? ')
    kernel = input()
    print('What would you like to use for gamma? ')
    gamma = float(input())
    print('What would you like to use for nu? ')
    nu = float(input())
elif default == 'y':
    kernel = 'rbf'
    gamma = 'scale'
    nu = 0.2

#Train model
model = api.train(train, kernel, gamma, nu)

#Get testing instructions
choice = ''
print('It is time to test the model!')
while choice != 'exit':
    print('\n\nYou can test as many times as you would like. To end the session with this model, input "exit"')
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
    if choice == 'self':
        print('\nInput the name of the label file for the training dataset: ')
        labelFile = input()
        print('\n--Testing against self--')
        api.testData(model, train, labelFile)
    elif choice == 'consensus':
        print('\n--Testing against consensus--')
        api.testData(model, api.prepFile('consensusTest.csv'), 'consensusTestLabels.csv')
    elif choice == 'mixNES':
        print('\n--Testing against mixNES--')
        api.testData(model, api.prepFile('mixNESTest.csv'), 'mixNESTestLabels.csv')
    elif choice == 'mixWithRandom':
        print('\n--Testing against mixWithRandom--')
        api.testData(model, api.prepFile('mixWithRandomTest.csv'), 'mixWithRandomTestLabels.csv')
    elif choice == 'mixAll':
        print('\n--Testing against mixAll--')
        api.testData(model, api.prepFile('mixAllTest.csv'), 'mixAllTestLabels.csv')
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
    elif choice == 'custom':
        print('\nInput the name of the test dataset: ')
        testData = input()
        print('Input the name of the label file for the test dataset: ')
        testLabel = input()
        print('\n--Testing against custom--')
        api.testData(model, api.prepFile(testData), testLabel)
    elif choice != 'exit':
        print('Sorry, that was not a valid option')
api.sys.exit()