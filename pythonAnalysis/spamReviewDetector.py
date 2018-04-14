#  from nltk import NaiveBayesClassifier
#  from nltk import FreqDist
import project_funclib

import nltk
import pickle
from random import shuffle
from pprint import pprint


def find_features(review, frequent_words):
    '''Find the which words in the review are contained within the word_features
    what were determined from the movie review dataset'''
    words = review.split()
    features = {}
    for word in frequent_words:
        features[word] = (word in words)
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
        text = review[0].replace('-', ' ').replace('/', ' ')
        if not isEnglish(text):
            continue
        documents.append((text, label))
        words = nltk.tokenize.word_tokenize(text)
        POS = nltk.tag.pos_tag(words)
        #  [print(word, tag) for word, tag in POS if tag.startswith('J')]
        [all_words.append(w.lower()) for w, tag in POS if tag.startswith('J')]
    return


#  data = DataFrame({'message': [], 'class': []})
documents = []
all_words = []
spam_query = 'SELECT text FROM review JOIN user\
         ON user.id=review.user_id WHERE review_count = 1\
         AND review.useful = 0 AND review.funny = 0 AND review.cool = 0 limit 1000'
#  data.append(data_frame_from_directory(query, '1'))
ham_query = 'SELECT text FROM review JOIN user\
         ON user.id=review.user_id WHERE review_count > 10 limit 1000'
#  data.append(data_frame_from_directory(query, '0'))
build_dataset_from_query(spam_query, documents, all_words, 'spam')
build_dataset_from_query(ham_query, documents, all_words, 'ham')

# list of all words of interest from reviews (determined by select_tags
all_words = nltk.FreqDist(all_words)
# Select the top N most frequent words from this list to select as words that
# indicate a review is spam
word_features = list(all_words.keys())[:5000]
feature_sets = [(find_features(review, word_features), category) for
                (review, category) in documents]
shuffle(feature_sets)
len_data = int(len(feature_sets) * 0.7)
training_set = feature_sets[:len_data]
testing_set = feature_sets[len_data:]
classifier = nltk.NaiveBayesClassifier.train(training_set)
print(nltk.classify.accuracy(classifier, testing_set))
classifier.show_most_informative_features(15)

#  with open('/home/josh/Documents/python/tensorflow/yelp/pickles/spamText.pickle'
#            , 'wb') as dataset_pkl:
#      pickle.dump(feature_sets, dataset_pkl)
#  with open('/home/josh/Documents/python/tensorflow/yelp/pickles/spamText.pickle'
#            , 'rb') as dataset_pkl:
#      data = pickle.load(dataset_pkl)
#  with open('/home/josh/Documents/python/tensorflow/yelp/pickles/spamText.pickle'
#            , 'wb') as dataset_pkl:
#      pickle.dump(feature_sets, dataset_pkl)
