# !/usr/bin/python

import mysql.connector
import matplotlib.pyplot as plt
from itertools import groupby

def open_conn():
    """open the connection before each test case"""
    conn = mysql.connector.connect(user='username', password='password',
                                   host='localhost',
                                   database='database_name')

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

if __name__ == '__main__':
    #open connection to the database
    conn = open_conn()
    
    #fetch results from the database
    result = executeQuery(conn, 'select c1 from t1 order by c1;')
    #retreive results as a list from the list of tuples
    result_list = [row[0] for row in result]
    freq_res = [len(list(group)) for key, group in groupby(result_list)]

    #plot results
    x = list(set(result_list))
    y = freq_res
    f, ax = plt.subplots(1)
    ax.plot(x, y)
    ax.set_ylim(ymin=0,ymax=5)
    plt.savefig('plot_frequency.png')

    #close connection to the database
    close_conn(conn)
