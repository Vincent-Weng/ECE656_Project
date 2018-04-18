import project_funclib

import nltk
import pickle
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
    print(nltk.classify.accuracy(classifier, testing_set))
    classifier.show_most_informative_features(15)


def gaussianNB_classifier(X_train, X_test, y_train, y_test):
    gaussian_nb_classifier = GaussianNB()
    gaussian_nb_classifier.fit(X_train, y_train)
    pred = gaussian_nb_classifier.predict(X_test)
    print('gaussianNB Accuracy score: {}'.format(accuracy_score(y_test, pred)))
    print('gaussianNB Precision score: {}'.format(precision_score(y_test, pred)))
    print('gaussianNB Recall score: {}'.format(recall_score(y_test, pred)))
    print('gaussianNB F1 score: {}'.format(f1_score(y_test, pred)))


def random_forest_classifier(X_train, X_test, y_train, y_test):
    classifier1 = RandomForestClassifier(n_estimators=15, criterion='entropy')
    classifier1.fit(X_train, y_train)
    predRF = classifier1.predict(X_test)
    print('RF Accuracy score: {}'.format(accuracy_score(y_test, predRF)))
    print('RF Precision score: {}'.format(precision_score(y_test, predRF)))
    print('RF Recall score: {}'.format(recall_score(y_test, predRF)))
    print('RF F1 score: {}'.format(f1_score(y_test, predRF)))


num_results = 1000
num_reviews = 10
age = 0

spam_query = 'SELECT text FROM review JOIN user\
         ON user.id=review.user_id WHERE review_count = 1\
         AND review.useful = 0 AND review.funny = 0 AND review.cool = 0\
         AND review.date - yelping_since = %d and (average_stars = 1 or\
         average_stars = 5) limit %d;' % (age, num_results)
ham_query = 'SELECT text FROM review JOIN user\
         ON user.id=review.user_id WHERE review_count > %d limit %d' % (num_reviews, num_results)

#  feature_sets = build_feature_set(spam_query, ham_query)
#  len_data = int(len(feature_sets) * 0.7)
#  training_set = feature_sets[:len_data]
#  testing_set = feature_sets[len_data:]
#  naive_bayes_classifier(training_set, testing_set)

x, y = build_rf_feature_set(spam_query, ham_query)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30)
gaussianNB_classifier(X_train, X_test, y_train, y_test)
random_forest_classifier(X_train, X_test, y_train, y_test)
