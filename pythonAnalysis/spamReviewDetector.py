import project_funclib

import nltk
import pickle
from matplotlib import pyplot
from random import shuffle
from pprint import pprint

from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


def find_features(review, frequent_words):
    '''Find the which words in the review are contained within the word_features
    what were determined from the movie review dataset'''
    words = review.split()
    features = dict.fromkeys(frequent_words, False)
    for word in words:
        if word in frequent_words:
            features[word] = True
    return features


def select_tags(pos): return pos[:2].startswith(("J"))


def isEnglish(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def build_dataset_from_query(query, documents, all_words, label):
    for review in project_funclib.executeQuery(query):
        text = review[0].replace('-', ' ').replace('/', ' ').replace('.', ' ').lower()
        if not isEnglish(text):
            continue
        documents.append((text, label))
        words = nltk.tokenize.word_tokenize(text)
        POS = nltk.tag.pos_tag(words)
        #  [print(word, tag) for word, tag in POS if tag.startswith('J')]
        [all_words.append(w.lower()) for w, tag in POS if tag.startswith('J')]
    return


def build_feature_set(spam_query, ham_query):
    documents = []
    all_words = []
    build_dataset_from_query(spam_query, documents, all_words, 'spam')
    build_dataset_from_query(ham_query, documents, all_words, 'ham')
    # list of all words of interest from reviews (determined by select_tags
    all_words = nltk.FreqDist(all_words)
    # Select the top N most frequent words from this list to select as words
    # that indicate a review is spam
    word_features = set(list(all_words.keys())[:5000])
    feature_sets = [(find_features(review, word_features), category) for
                    (review, category) in documents]
    shuffle(feature_sets)
    return feature_sets


def build_rf_feature_set(spam_query, ham_query):
    documents = []
    all_words = []
    y = []
    orpus = []
    build_dataset_from_query(spam_query, documents, all_words, 'spam')
    build_dataset_from_query(ham_query, documents, all_words, 'ham')
    for text, label in documents:
        y.append(label)
        orpus.append(text)
    cv = CountVectorizer(max_features=5000)
    x = cv.fit_transform(orpus).toarray()
    le = LabelEncoder()
    y = le.fit_transform(y)
    return x, y


def naive_bayes_classifier(training_set, testing_set):
    classifier = nltk.NaiveBayesClassifier.train(training_set)
    accuracy = nltk.classify.accuracy(classifier, testing_set)
    #  classifier.show_most_informative_features(15)
    return accuracy


def random_forest_classifier(X_train, X_test, y_train, y_test):
    classifier1 = RandomForestClassifier(n_estimators=15, criterion='entropy')
    classifier1.fit(X_train, y_train)
    predRF = classifier1.predict(X_test)
    print('RF Accuracy score: {}'.format(accuracy_score(y_test, predRF)))
    print('RF Precision score: {}'.format(precision_score(y_test, predRF)))
    #  print('RF Recall score: {}'.format(recall_score(y_test, predRF)))
    #  print('RF F1 score: {}'.format(f1_score(y_test, predRF)))


def train_classifiers(category, ages, num_results, num_reviews):
    spam_query = "SELECT text FROM (SELECT text, business_id, user_id, date from review \
            WHERE useful = 0 AND funny = 0 AND cool = 0) as c JOIN\
            (SELECT id, yelping_since from user where average_stars = (5 or 1) AND review_count = 1)\
            AS a ON a.id=c.user_id JOIN (select business_id from category WHERE\
            category = '%s') as b USING(business_id) WHERE\
            c.date - a.yelping_since BETWEEN %d and %d limit %d;"\
            % (category, ages[0]*10000000000, ages[1]*10000000000, num_results)
    ham_query = "SELECT text FROM review JOIN (select id from user where\
            review_count > %d) as a ON a.id=review.user_id JOIN (SELECT\
            business_id from category where category='%s') as b on\
            review.business_id=b.business_id limit %d" % (num_reviews, category, num_results)

    feature_sets = build_feature_set(spam_query, ham_query)
    len_data = int(len(feature_sets) * 0.7)
    training_set = feature_sets[:len_data]
    testing_set = feature_sets[len_data:]
    return naive_bayes_classifier(training_set, testing_set)

    #  x, y = build_rf_feature_set(spam_query, ham_query)
    #  X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
    #  random_forest_classifier(X_train, X_test, y_train, y_test)

num_results = 1000
age = (0, 0)
category = 'Restaurants'  # , 'Health & Medical', 'Shopping'
num_reviews = 10

#  accuracy = []
#  for num_reviews in range(0, 101, 10):
#      accuracy.append(train_classifiers(category, age, num_results, num_reviews))

#  pyplot.figure(1)
#  pyplot.plot(range(0, 101, 10), accuracy)
#  pyplot.xlabel('review_count by User')
#  pyplot.ylabel('Spam Detection Accuracy')

accuracy = []
ages_high = [0]
ages_low = [0]
[ages_high.append(i) for i in range(11)]
[ages_low.append(i) for i in range(1, 12)]
for age_low, age_high in zip(ages_low, ages_high):
    ages = (age_low, age_high)
    accuracy.append(train_classifiers(category, ages, num_results, num_reviews))

pyplot.figure(2)
pyplot.plot([(i,j) for i, j in zip(ages_low, ages_high)], accuracy)
pyplot.xlabel('Time Between Account Creation and First Review (days)')
pyplot.ylabel('Spam Detection Accuracy')

#  accuracy = []
#  categories = ['Restaurants', 'Health & Medical', 'Shopping', 'Beauty & Spas',
#                'Home Services', 'Nightlife', 'Automotive']
#  for category in categories:
#      accuracy.append(train_classifiers(category, age, num_results, num_reviews))

#  pyplot.figure(3)
#  pyplot.plot(categories, accuracy)
#  pyplot.xlabel('Business Category')
#  pyplot.ylabel('Spam Detection Accuracy')
pyplot.show()
