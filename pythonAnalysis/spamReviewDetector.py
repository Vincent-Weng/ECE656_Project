import project_funclib

import pymysql
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


def isEnglish(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def build_dataset_from_query(query, documents, all_words, label):
    '''Takes in the raw data from the SQL query and performs POS tagging as well as
    cleans the data to remove foreign language reviews and symbols'''
    for review in project_funclib.executeQuery(query):
        text = review[0].replace('-', ' ').replace('/', ' ').replace('.', ' ').lower()
        if not isEnglish(text):
            continue
        documents.append((text, label))
        words = nltk.tokenize.word_tokenize(text)
        POS = nltk.tag.pos_tag(words)
        #  [print(word, tag) for word, tag in POS if tag.startswith('J')]
        [all_words.append(w.lower()) for w, tag in POS if tag.startswith(('J', 'R'))]
    return


def build_feature_set(spam_query, ham_query):
    '''Takes in the raw data from the SQL query and formats it correctly for
    the NLTK classifier'''
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


def build_sk_feature_set(spam_query, ham_query):
    '''Takes in the raw data from the SQL query and formats it correctly for
    the sklearn classifiers'''
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
    #  classifier.show_most_informative_features(5)
    return accuracy


def gaussianNB_classifier(X_train, X_test, y_train, y_test):
    '''Applies sklearn's gaussianNB algorithm to the feature set'''

    gaussian_nb_classifier = GaussianNB()
    gaussian_nb_classifier.fit(X_train, y_train)
    pred = gaussian_nb_classifier.predict(X_test)
    print('gaussianNB Accuracy score: {}'.format(accuracy_score(y_test, pred)))
    print('gaussianNB Precision score: {}'.format(precision_score(y_test, pred)))
    print('gaussianNB Recall score: {}'.format(recall_score(y_test, pred)))
    print('gaussianNB F1 score: {}'.format(f1_score(y_test, pred)))


def random_forest_classifier(X_train, X_test, y_train, y_test):
    '''Applies sklearn's random forest algorithm to the feature set'''

    classifier1 = RandomForestClassifier(n_estimators=15, criterion='entropy')
    classifier1.fit(X_train, y_train)
    predRF = classifier1.predict(X_test)
    print('RF Accuracy score: {}'.format(accuracy_score(y_test, predRF)))
    print('RF Precision score: {}'.format(precision_score(y_test, predRF)))
    print('RF Recall score: {}'.format(recall_score(y_test, predRF)))
    print('RF F1 score: {}'.format(f1_score(y_test, predRF)))


def train_classifiers(category, ages, num_results, avg_stars):
    '''Executes the SQL queries to get the necessary data and calls the
    classification algorithms on the data after it is formatted correctly'''

    spam_query = "SELECT text FROM (SELECT text, business_id, user_id, date from review \
            WHERE useful = 0 AND funny = 0 AND cool = 0) as c JOIN\
            (SELECT id, yelping_since from user WHERE average_stars %s)\
            AS a ON a.id=c.user_id JOIN (select business_id\
            from category WHERE category = '%s') as b USING(business_id) WHERE\
            c.date - a.yelping_since BETWEEN %d and %d limit %d;"\
            % (avg_stars, category, ages[0]*10000000000, ages[1]*10000000000, num_results)
    ham_query = "SELECT text FROM review JOIN (select id from user where\
            review_count > 10) as a ON a.id=review.user_id JOIN (SELECT\
            business_id from category where category='%s') as b on\
            review.business_id=b.business_id limit %d" % (category, num_results)
    # Build the feature sets from the reviews returned by each query
    # They will each be labeled spam or ham (ham are not spam)
    feature_sets = build_feature_set(spam_query, ham_query)
    len_data = int(len(feature_sets) * 0.5)
    training_set = feature_sets[:len_data]
    testing_set = feature_sets[len_data:]
    # These are additional classification algorithms that were tried but
    # removed to speed up computation time
    #  x, y = build_sk_feature_set(spam_query, ham_query)
    #  X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
    #  random_forest_classifier(X_train, X_test, y_train, y_test)
    #  gaussianNB_classifier(X_train, X_test, y_train, y_test)
    return naive_bayes_classifier(training_set, testing_set)


avg_stars = '=(1 or 5)'
num_results = 1000  # Total number of results to analyze from each query to speed up execution
age = (0, 0)  # The time between account creation and the first review for accounts with 1 review
category = 'Restaurants'  # The category of businesses to analyze

# Analyze the number of reviews between 2 and 101 as the minimum required to not be spam
#  accuracy = []
#  avg_star = ['=1'
#              ,'BETWEEN 1 AND 2'
#              ,'BETWEEN 1 AND 3'
#              ,'BETWEEN 1 AND 4'
#              ,'BETWEEN 1 AND 5'
#              ]
#  for low_high_star in avg_star:
#      accuracy.append(train_classifiers(category, age, num_results, low_high_star))

#  pyplot.figure(1)
#  pyplot.plot(avg_star, accuracy)
#  pyplot.xlabel('average_stars Range for User')
#  pyplot.ylabel('Spam Detection Accuracy')

# Analyze ages of reviews between 0 and 7 days, with 0 having the biggest population
accuracy = []
ages_high = [0]
ages_low = [0]
[ages_low.append(i) for i in range(6)]
[ages_high.append(i) for i in range(1, 7)]
for age_low, age_high in zip(ages_low, ages_high):
    ages = (age_low, age_high)
    print(ages)
    accuracy.append(train_classifiers(category, ages, num_results, avg_stars))

pyplot.figure(2)
pyplot.plot(ages_low, accuracy)
pyplot.xlabel('Time Between Account Creation and First Review (days)')
pyplot.ylabel('Spam Detection Accuracy')

#  # Analyze the accuracy of spam detection across different categories of businesses
#  accuracy = []
#  categories = ['Restaurants', 'Health & Medical', 'Shopping', 'Beauty & Spas',
#                'Home Services', 'Nightlife', 'Automotive']
#  for category in categories:
#      accuracy.append(train_classifiers(category, age, num_results, avg_stars))

#  pyplot.figure(3)
#  pyplot.plot(categories, accuracy)
#  pyplot.xlabel('Business Category')
#  pyplot.ylabel('Spam Detection Accuracy')
pyplot.show()
