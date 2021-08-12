from sklearn.metrics import classification_report
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import csv
import warnings
import numpy as np
from nltk_utils import bag_of_words, tokenize, stem
from prep import getTestData, getPrepResponse
# load data using pandas
# data = pd.read_csv("dataset.tsv", sep="\t")
# print(data['label'].value_counts())
# print(data.shape)
# dataset has 254 rows and 2 columns
# 10 different labels

label = []
utterance = []
stopWords = list(set(stopwords.words('english')))
porter = PorterStemmer()
# read data
# Get the data
dataset = open('train.tsv')
read = csv.reader(dataset, delimiter='\t')
next(read,None)

data = []
stopWords = list(set(stopwords.words('english')))


# All unique tokens [token, token, token]
all_words = []

# Unique tags [tag, tag, ...]
tags = []

# Target: [(['hello'], 'greetings'), (['hey'], 'greetings'), (['hi'], 'greetings'), (['greetings'], 'greetings'),
# Which is [([token, token, ...], tag)]
xy = []

# Get the data
X_train, y_train, all_words, tags, xy = getTestData()
# print(X_train)
# print(y_train)
# svm model
svm_model = svm.SVC(kernel='linear').fit(X_train, y_train)
nb_model = MultinomialNB().fit(X_train, y_train)
# print(svm_model)

def svm(utterance):
    X = getPrepResponse(utterance, all_words)
    return svm_model.predict(X)[0]

def MultiNB(utterance):
    X = getPrepResponse(utterance, all_words)
    return nb_model.predict(X)[0]

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
        y_pred.append(tags[(svm(i))])
        #y_pred.append(tags[(MultiNB(i))])
    # print(y_test)
    # print(y_pred)
    warnings.filterwarnings("ignore")
    print(classification_report(y_test, y_pred))

# classReport()