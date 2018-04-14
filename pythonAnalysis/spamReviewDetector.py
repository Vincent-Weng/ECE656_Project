#  from nltk import NaiveBayesClassifier
#  from nltk import FreqDist
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pymysql
from pandas import DataFrame
from pprint import pprint
import pickle
from random import shuffle


def open_conn():
    """open the connection before each test case"""
    conn = pymysql.connect(user='public', password='ece656yelp',
                           host='maindb.czbva1am4d4u.us-east-2.rds.amazonaws.com',
                           database='yelp_db')
    return conn


def close_conn(conn):
    """close the connection after each test case"""
    conn.close()


def executeQuery(query, commit=False):
    """ fetch result after query"""
    conn = open_conn()
    cursor = conn.cursor()
    query_num = query.count(";")
    if query_num > 1:
        for result in cursor.execute(query, params=None, multi=True):
            if result.with_rows:
                result = result.fetchall()
    else:
        cursor.execute(query)
        result = cursor.fetchall()
    # we commit the results only if we want the updates to the database
    # to persist.
    if commit:
        conn.commit()
    else:
        conn.rollback()
    # close the cursor used to execute the query
    cursor.close()
    close_conn(conn)
    return result


def data_frame_from_directory(query, classification):
    rows = []
    for message in executeQuery(query):
        trimmed_message = message[0].replace('\n', ' ')
        rows.append({'message': trimmed_message, 'class': classification})
    return rows


def find_features(review, frequent_words):
    '''Find the which words in the review are contained within the word_features\
    what were determined from the movie review dataset'''
    words = review.split()
    features = {}
    for word in frequent_words:
        features[word] = (word in words)
    return features


def is_adj_or_adv(pos): return pos[:2].startswith(("J", "R"))


#  data = DataFrame({'message': [], 'class': []})
documents = []
all_words = []
spam_query = 'SELECT text FROM review JOIN user\
         ON user.id=review.user_id WHERE review_count = 1 limit 10000'
#  data.append(data_frame_from_directory(query, '1'))
ham_query = 'SELECT text FROM review JOIN user\
         ON user.id=review.user_id WHERE review_count > 10 limit 10000'
#  data.append(data_frame_from_directory(query, '0'))
for review in executeQuery(spam_query):
    text = review[0]
    documents.append((text, "spam"))
    words = nltk.tokenize.word_tokenize(text)
    POS = nltk.pos_tag(words)
    [all_words.append(w[0].lower()) for w in POS if is_adj_or_adv(w[1])]
for review in executeQuery(spam_query):
    text = review[0]
    documents.append((text, "ham"))
    words = nltk.tokenize.word_tokenize(text)
    POS = nltk.pos_tag(words)
    [all_words.append(w[0].lower()) for w in POS if is_adj_or_adv(w[1])]
all_words = nltk.FreqDist(all_words)
word_features = list(all_words.keys())[:1000]
feature_sets = [(find_features(review, word_features), category) for
                (review, category) in documents]
shuffle(feature_sets)
len_data = int(len(feature_sets) * 0.7)
training_set = feature_sets[:len_data]
testing_set = feature_sets[len_data:]


with open('/home/josh/Documents/python/tensorflow/yelp/pickles/spamText.pickle'
          , 'wb') as dataset_pkl:
    pickle.dump(feature_sets, dataset_pkl)
#  with open('/home/josh/Documents/python/tensorflow/yelp/pickles/spamText.pickle'
#            , 'rb') as dataset_pkl:
#      data = pickle.load(dataset_pkl)

#  vectorizer = CountVectorizer()
#  counts = vectorizer.fit_transform(data['message'].values)
#  targets = data['class'].values
#  classifier.fit(counts, targets)
#  example_counts = vectorizer.transform(examples)
#  predictions = classifier.predict(example_counts)
classifier = nltk.NaiveBayesClassifier.train(training_set)
classifier.show_most_informative_features(5)
print(nltk.classify.accuracy(classifier, testing_set))


#  # runs once on training data
#  def train(trainData):
#      total = 0
#      numSpam = 0
#      # Emails labeled with 1 if spam, 0 otherwise
#      for email in trainData:
#          if email.label == 1:
#              numSpam += 1
#          total += 1
#          processEmail(email.body, email.label)
#      pA = numSpam/float(total)
#      pNotA = (total - numSpam)/float(total)


#  def processEmail(body, label):
#      '''counts the words in a specific email'''
#      for word in body:
#          if label == SPAM:
#              trainPositive[word] = trainPositive.get(word, 0) + 1
#              positiveTotal += 1
#          else:
#              trainNegative[word] = trainNegative.get(word, 0) + 1
#              negativeTotal += 1


#  def conditionalWord(word, spam):
#      '''gives the conditional probability p(B_i | A_x)'''
#      if spam:
#          return trainPositive[word]/float(positiveTotal)
#      return trainNegative[word]/float(negativeTotal)


#  #gives the conditional probability p(B | A_x)
#  def conditionalEmail(body, spam):
#      result = 1.0
#      for word in body:
#          result *= conditionalWord(word, spam)
#      return result


#  #classifies a new email as spam or not spam
#  def classify(email):
#      isSpam = pA * conditionalEmail(email, True) # P (A | B)
#      notSpam = pNotA * conditionalEmail(email, False) # P(¬A | B)
#      return isSpam > notSpam
