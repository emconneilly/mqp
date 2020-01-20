# Runnable Tool that takes prompts the user for input to train and test an OC SVM Model

import ocsvmAPI as api 

#Get data
print('Welcome to the NES Model Training Tool! To train and test the model, please follow along.')
print('Input the name of the training dataset: ')
trainRaw = input()

#Prep data
train = api.prepFile(trainRaw)

#Explain parameters
print("This model requires some parameters to be set. These include a kernel, gamma, and nu.")
print("Would you like these to be explained in more detail? (y/n)")
explain = input()
if explain = 'y':
    print("The kernel is the function the model will use to transform the data if it needs to be fit in a higher dimension.")
    print("When the data does not need to be fit in a higher dimension, a linear kernel will fit the data as is.\n")
    print("Gamma is a representation of the impact of each training value on the model's fit.")
    print("A higher gamma means each value has less influence and a lower gamma means each value has more influence.\n")
    print("Nu is the upper bound of the proportion of training values that the model can label as an incorrect group.\n")

#Get parameters
print("Some parameters have been chosen through iterative testing as defaults.")
print("The default parameters are kernel=rbf, gamma=1/number of features, nu=0.2")
print('Would you like to use the default parameters? (y/n) ')
default = input()
if default == 'n':
    print('What would you like to set as the kernel? ')
    print("The options are linear, poly, rbf, or sigmoid")
    kernel = input()
    print('What would you like to use for gamma? ')
    print("It should be a number in the range (0,1]")
    gamma = float(input())
    print('What would you like to use for nu?')
    print("It must be a number in the range (0,1]")
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