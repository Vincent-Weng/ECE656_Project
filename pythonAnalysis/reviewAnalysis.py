import matplotlib.pyplot as plt
import pandas
import project_funclib
from collections import Counter


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
    # Clearing key-value pairs that don't pass a threshold
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
    reviews = project_funclib.fetchData(query, 'query_text')

    word_count = countWords(reviews, 10)
    trimmed_word_count = removeWords(word_count, 5)

    print('Finished counting words, displaying...')
    s = pandas.Series(trimmed_word_count)
    s = s.sort_values(ascending=False)
    s.plot(kind='bar')
    plt.savefig("keyword_plot.pdf", format="pdf")
