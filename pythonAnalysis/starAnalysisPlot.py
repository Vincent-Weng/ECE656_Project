import project_funclib

import os
import matplotlib.pyplot as plt
from pprint import pprint
from collections import Counter


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
    avg = sum(diff) / len(diff)

    m = [[val_list[0]]]

    for x in val_list[1:]:
        if x - m[-1][0] < avg:
            m[-1].append(x)
        else:
            m.append([x])
    return m


def split_by_stars(val_list):
    output = [[] for _ in range(5)]
    [output[val-1].append(age) for age, val in val_list]
    return output


def split_by_age(grouped_ages_by_stars):
    i = 0
    buckets = []
    if grouped_ages_by_stars:
        buckets.append([grouped_ages_by_stars[0]])
    else:
        return grouped_ages_by_stars
    # Start for loop at 1 since first value was added already
    for j in range(1, len(grouped_ages_by_stars)):
        # get the lowest age and see if any values are within 5000000000 of it
        if grouped_ages_by_stars[j] - buckets[i][0] > 5000000000:
            # value too large, creates new bucket
            i += 1
            buckets.append([grouped_ages_by_stars[j]])
        else:
            # value within bucket size, add it
            buckets[i].append(grouped_ages_by_stars[j])
    return buckets


def groupKeys(val_list):
    # sort the list of tuples by their first val (the age of review since
    # when an account was opened)
    val_list.sort()
    final_buckets = [[] for _ in range(5)]
    buckets = split_by_stars(val_list)
    ages = set()
    # determine frequency that star rating occurs on each age and normalize
    # frequency for each age by dividing by the max frequency for that age
    for star in range(5):
        split_buckets = split_by_age(buckets[star])
        for i in range(len(split_buckets)):
            sum_age = sum(split_buckets[i])
            count = len(split_buckets[i])
            avg_age = int((sum_age/count) / 8872000000)
            ages.add(avg_age)
            final_buckets[star].append([avg_age, count])
    # Add freq values of 0 to stars at an age that doesn't have a value
    for star in range(5):
        for _age in ages:
            if _age not in [_avg_age for _avg_age, freq in final_buckets[star]]:
                final_buckets[star].append([_age, 0])
        final_buckets[star].sort()
    # Normalize freq to 1
    for i in range(len(final_buckets[0])):
        max_freq = 0
        for star in range(5):
            if final_buckets[star][i][1] > max_freq:
                max_freq = final_buckets[star][i][1]
        for star in range(5):
            final_buckets[star][i][1] /= max_freq
    return final_buckets


def grouped_bar_plot(grouped_ages):
    fig, ax = plt.subplots()
    width = 0.1
    ind = [age for age, freq in grouped_ages[0]]
    for i in range(5):
        ax.bar([val + width*(i-1) for val in ind]
               , [count for age, count in grouped_ages[i]]
               , width
               )
    plt.xlabel('Age of comment (days)')
    plt.ylabel('Freq')
    plt.legend(('1 Star', '2 Star', '3 Star', '4 Star', '5 Star'))
    plt.savefig("star_plot.pdf", format="pdf")
    plt.show()


if __name__ == '__main__':
    query = 'SELECT date - yelping_since as age, stars FROM review JOIN user\
            ON user.id=review.user_id limit 100000'
    # Warning, data is cached so changing query wont do anything unless cache
    # is cleared by deleting query_test.txt file or writing to a new file
    result = list(project_funclib.executeQuery(query))
    grouped_ages = groupKeys(result)
    grouped_bar_plot(grouped_ages)
