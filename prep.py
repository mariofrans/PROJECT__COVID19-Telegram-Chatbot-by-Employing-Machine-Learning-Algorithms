import csv
import numpy as np
from nltk_utils import bag_of_words, tokenize, stem
from nltk.corpus import stopwords
stopWords = list(set(stopwords.words('english')))


# Prepping the data for all algorithms
def getTestData():
    data = []
    # All unique tokens [token, token, token]
    all_words = []
    # Unique tags [tag, tag, ...]
    tags = []
    # Target: [(['hello'], 'greetings'), (['hey'], 'greetings'), (['hi'], 'greetings'), (['greetings'], 'greetings'),
    # Which is [([token, token, ...], tag)]
    xy = []

    # Get the data
    file = open('train.tsv')
    read = csv.reader(file, delimiter='\t')
    next(read,None)

    for i in read:
        # Get unique tags
        if i[0] not in tags:
            tags.append(i[0])
        data.append(i)


    # Tokenize all possible words
    for sentence in data:
        tempTag = sentence[0]
        tempSen = []
        for word in tokenize(sentence[1]):
            if word not in (stopWords + ['.', ',', '?']):
                stemmed = stem(word.lower())
                tempSen.append(stemmed)
                if stemmed not in all_words:
                    all_words.append(stemmed)
        xy.append((tempSen, tempTag))

    # create training data
    X_train = []
    y_train = []
    for (pattern_sentence, tag) in xy:
        # X: bag of words for each pattern_sentence
        bag = bag_of_words(pattern_sentence, all_words)
        X_train.append(bag)
        # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
        label = tags.index(tag)
        y_train.append(label)


    X_train = np.array(X_train)
    y_train = np.array(y_train)

    return X_train, y_train, all_words, tags, xy

def getPrepResponse(userResponse, all_words):
    tokenizedResponse = []
    for word in tokenize(userResponse):
        if word not in (stopWords + ['.', ',', '?']):
            tokenizedResponse.append(stem(word.lower()))
    # print(userResponse)
    X = bag_of_words(tokenizedResponse, all_words)
    X = X.reshape(1, X.shape[0])
    return X

# X_train, y_train, all_words, data = getTestData()

# X = getPrepResponse('How many cases in US?', all_words)
# print(X)