import requests
import json
import torch
import random
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize, stem
from prep import getPrepResponse
from nltk.corpus import stopwords
from sklearn.metrics import classification_report
import csv
import pycountry
import warnings


stopWords = list(set(stopwords.words('english')))


def predict(userResponse):
    # start chat function
    # userResponse = 'what is covid?'
    countryList = []
    tokenizedResponse = []
    for country in pycountry.countries:
        if country.name in userResponse:
            countryList.append(country.name)
        elif country.alpha_3 in userResponse:
            countryList.append(country.alpha_3)
            
    # ===============================================================================
    # Load model??
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    FILE = "data.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model = NeuralNet(input_size, hidden_size, output_size).to(device)
    model.load_state_dict(model_state)
    model.eval()
    # ===============================================================================

    # Prepping the input ??
    X = getPrepResponse(userResponse, all_words)
    X = torch.from_numpy(X).to(device)
    # ===============================================================================

    # Predicting??
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    # ===============================================================================
    if prob.item() > 0.75:
        # # if tag == 'Case_Count':
        # output = handler(tag, countryList)
        output = tag
    else:
        # output = 'I dont understand'
        output = tag
    return output

def classReport():
    # Get the test data
    file = open('test.tsv')
    read = csv.reader(file, delimiter='\t')
    next(read,None)

    X_test = []
    y_test = []

    for i in read:
        X_test.append(i[1])
        y_test.append(i[0])

    y_pred = []

    for i in X_test:
        y_pred.append(predict(i))

    warnings.filterwarnings("ignore")
    print(classification_report(y_test, y_pred))

# classReport()