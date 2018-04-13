import matplotlib.pyplot as plt
from pprint import pprint
from project_funclib import *


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
