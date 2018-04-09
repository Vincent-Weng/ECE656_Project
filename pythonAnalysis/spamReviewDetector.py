#  from nltk import NaiveBayesClassifier
#  from nltk import FreqDist
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import pymysql
from pandas import DataFrame
from pprint import pprint
import pickle


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
        pprint(trimmed_message)
        rows.append({'message': trimmed_message, 'class': classification})
    return DataFrame(rows)


data = DataFrame({'message': [], 'class': []})
query = 'SELECT text as age FROM review JOIN user\
         ON user.id=review.user_id WHERE review_count = 1 limit 100'
data.append(data_frame_from_directory(query, '1'))
query = 'SELECT text as age FROM review JOIN user\
         ON user.id=review.user_id WHERE review_count > 10 limit 100'
data.append(data_frame_from_directory(query, '0'))
with open('/home/josh/Documents/python/tensorflow/yelp/pickles/spamText.pickle'
          , 'wb') as dataset_pkl:
    pickle.dump(data, dataset_pkl)
#  with open('/home/josh/Documents/python/tensorflow/yelp/pickles/spamText.pickle'
#            , 'rb') as dataset_pkl:
#      data = pickle.load(dataset_pkl)

vectorizer = CountVectorizer()
counts = vectorizer.fit_transform(data['message'].values)
classifier = MultinomialNB()
targets = data['class'].values
classifier.fit(counts, targets)
examples = ['Free viagra now!!!', 'Hi Bob, how about a game of golf tomorrow?']
example_counts = vectorizer.transform(examples)
predictions = classifier.predict(example_counts)
print(predictions)


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
