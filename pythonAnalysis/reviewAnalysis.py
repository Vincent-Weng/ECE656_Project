"""Display settings"""
from IPython.display import HTML, display
import tabulate
import pymysql
import matplotlib.pyplot as plt
import pandas
from collections import Counter
from collections import OrderedDict
from pprint import pprint


def displayResult(queryResult, heading=()):
    if heading != ():
        resultList = (heading,) + queryResult
        display(HTML(tabulate.tabulate(
            [result for result in resultList], tablefmt='html')))
    else:
        display(HTML(tabulate.tabulate(
            [result for result in queryResult], tablefmt='html')))


"""MySQL connection related functions and variables"""


def open_conn():
    """open the connection before each test case"""
    conn = pymysql.connect(user='public', password='ece656yelp',
                           host='maindb.czbva1am4d4u.us-east-2.rds.amazonaws.com',
                           database='yelp_db')
    return conn


def close_conn(conn):
    """close the connection after each test case"""
    conn.close()


def executeQuery(conn, query, commit=False):
    """ fetch result after query"""
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
    return result


def fetchData(query, fileName):
    # Fetches the data from the SQL database and write the output to a text
    # file to open later to save time if were repeating the same queries
    try:
        reviews = open('%s.txt'
                       % fileName, 'r')
    except FileNotFoundError:
        # fetch results from the database
        conn = open_conn()
        print('query not found, fetching...')
        result = executeQuery(conn, query)
        # retreive results as a list from the list of tuples
        result_list = [row[0] for row in result]
        output_file = open('%s.txt'
                           % fileName, 'w')
        [output_file.write(review) for review in result_list]
        output_file.close()
        reviews = open('%s.txt'
                       % fileName, 'r')
        # close connection to the database
        close_conn(conn)
    return reviews


def countWords(textFile, numReviews):
    # Takes in a text file and returns a Counter object which contains
    # each word and the number of times it appears in the reviews
    word_counts = Counter()
    i = 0
    while i < numReviews:
        review = textFile.readline()
        if review is not '':
            word_counts = word_counts + Counter(review.split())
        i = i + 1
    return word_counts


def removeWords(word_counts, threshold):
    # Clearing key-value pairs that dont pass a threshold
    for key in list(word_counts):
        if word_counts[key] < threshold:
            del word_counts[key]
    return word_counts


if __name__ == '__main__':
    query = 'SELECT text FROM review JOIN user ON user.id=review.user_id\
            WHERE date = yelping_since AND review_count = 1 AND review.useful = 0\
            AND review.funny = 0 AND review.cool = 0;'
    # Warning, data is cached so changing query wont do anything unless cache
    # is cleared by deleting query_test.txt file or writing to a new file
    reviews = fetchData(query, 'query_text')

    word_count = countWords(reviews, 10)
    trimmed_word_count = removeWords(word_count, 5)

    print('Finished counting words, displaying...')
    s = pandas.Series(trimmed_word_count)
    s = s.sort_values(ascending=False)
    s.plot(kind='bar')
    plt.show()
