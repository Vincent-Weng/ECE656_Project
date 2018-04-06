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
        reviews = open('/home/josh/Documents/python/yelp-challenge/%s.txt'
                       % fileName, 'r')
        if(reviews.read() == ''):
            raise FileNotFoundError
    except FileNotFoundError:
        # fetch results from the database
        conn = open_conn()
        print('query not found, fetching...')
        result = executeQuery(conn, query)
        # retreive results as a list from the list of tuples
        #  result_list = [row[0] for row in result]
        result_list = result
        with open('/home/josh/Documents/python/yelp-challenge/%s.txt'
                % fileName, 'w') as output_file:
            [output_file.write(result) for result in result_list]
        reviews = open('/home/josh/Documents/python/yelp-challenge/%s.txt'
                       % fileName, 'r')
        # close connection to the database
        close_conn(conn)
    return reviews


def countWords(textFile, numReviews):
    """Takes in a text file and returns a Counter object which contains
    each word and the number of times it appears in the reviews"""
    word_counts = Counter()
    i = 0
    while i < numReviews:
        review = textFile.readline()
        if review is not '':
            word_counts = word_counts + Counter(review.split())
        i = i + 1
    return word_counts


def removeWords(word_counts, threshold):
    """Clearing key-value pairs that dont pass a threshold"""
    for key in list(word_counts):
        if word_counts[key] < threshold:
            del word_counts[key]
    return word_counts


def groupValues(val_list: list):
    """Takes a list and groups together the values that are close
    together and returns a list of lists"""
    val_list.sort()
    diff = [y - x for x, y in zip(*[iter(val_list)] * 2)]
    pprint(diff)
    avg = sum(diff) / len(diff)

    m = [[val_list[0]]]

    for x in val_list[1:]:
        if x - m[-1][0] < avg:
            m[-1].append(x)
        else:
            m.append([x])
    return m


def groupKeys(val_list: list):
    # sort the list of tuples by theiuri first val (the age of review since
    # when an account was opened)
    val_list.sort()
    # get the lowest age and see if any values are within 8000000000 of it
    curr_bucket = val_list[0][0]
    buckets = [[val_list[0]]]
    final_buckets = []
    color = []
    i = 0
    for val in val_list:
        if val[0] == curr_bucket:
            continue
        elif val[0] - curr_bucket < 5000000000:
            buckets[i].append(val)
        else:
            curr_bucket = val[0]
            buckets.append([val])
            i = i + 1

    for i in range(len(buckets)):
        for val in range(1, 6):
            count = 0
            sum_age = 0
            for age, tplVal in buckets[i]:
                if tplVal == val:
                    count = count + 1
                    sum_age = sum_age + age
            try:
                avg_age = float(sum_age/(count*1000000000))
                final_buckets.append((avg_age, val))
                color.append(count)
            except ZeroDivisionError:
                continue
    return final_buckets, color


if __name__ == '__main__':
    query = 'SELECT date - yelping_since as age, stars FROM review JOIN user\
            ON user.id=review.user_id limit 100000'

    # Warning, data is cached so changing query wont do anything unless cache
    # is cleared by deleting query_test.txt file or writing to a new file
    #  reviews = fetchData(query, 'review_age')
    conn = open_conn()
    result = list(executeQuery(conn, query))
    close_conn(conn)

    grouped_ages, size = groupKeys(result)
    ages_Dict = dict(grouped_ages)

    # word_count = countWords(reviews, 10)
    # trimmed_word_count = removeWords(word_count, 5)

    print('Finished counting words, displaying...')
    #  s = pandas.DataFrame(list(resultDict.items()), columns=['Time', 'Stars'])
    #  s.plot(kind='scatter')
    x = ages_Dict.keys()
    y = ages_Dict.values()
    norm_size = max(size)/100
    size = [size[i]/norm_size for i in range(len(size))]
    print(size)
    plt.scatter(x, y, s=size)
    plt.xlabel('Age of comment')
    plt.ylabel('Stars')
    plt.show()
