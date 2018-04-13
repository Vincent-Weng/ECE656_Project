import matplotlib.pyplot as plt
import pandas
from project_funclib import *

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
    plt.savefig("keyword_plot.pdf", format="pdf")
