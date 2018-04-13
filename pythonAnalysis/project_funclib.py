from IPython.display import HTML, display
import tabulate
import pymysql
import io


encoding = 'utf-8'

"""Display settings"""


def displayResult(queryResult, heading=()):
    if heading != ():
        resultList = (heading,) + queryResult
        display(HTML(tabulate.tabulate([result for result in resultList], tablefmt='html')))
    else:
        display(HTML(tabulate.tabulate([result for result in queryResult], tablefmt='html')))


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
        reviews = io.open('%s.txt'
                          % fileName, 'r', encoding=encoding)
    except FileNotFoundError:
        # fetch results from the database
        conn = open_conn()
        print('query not found, fetching...')
        result = executeQuery(conn, query)
        # retrieve results as a list from the list of tuples
        result_list = [row[0] for row in result]
        output_file = io.open('%s.txt'
                              % fileName, 'w', encoding=encoding)
        for review in result_list:
            output_file.write(review)
        output_file.close()
        reviews = io.open('%s.txt'
                          % fileName, 'r', encoding=encoding)
        # close connection to the database
        close_conn(conn)
    return reviews



