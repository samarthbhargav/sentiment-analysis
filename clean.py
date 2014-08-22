import os
import re
import collections
import nltk
import random

class Cleaner(object):

    stop_words = nltk.corpus.stopwords.words('english')

    delim = " "

    @staticmethod
    def remove_stop_words(text):
        new_text = []
        for word in text.split(Cleaner.delim):
            if word not in Cleaner.stop_words and len(word) > 0:
                new_text.append(word)
        return Cleaner.delim.join(new_text)

    @staticmethod
    def strip_special_chars(text):
        delim = Cleaner.delim
        replace_map = [
            ("\n\t", delim), # remove new lines and tabs
            (r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+" , delim), # remove urls, todo get domain name
            (r"[^0-9a-zA-Z#]" , delim), # remove non alphanumeric chars, also don't remove #
            ( "[{}][{}]+".format(delim,delim), delim ) # compress spaces
        ]
        replace_map = collections.OrderedDict(replace_map)
        for key in replace_map.keys():
            text = re.sub(key, replace_map[key], text)
        return text.strip()

    @staticmethod
    def remove_n_letter_chars(text, minlen):
        delim = Cleaner.delim
        new_text = []
        for word in text.split(delim):
            if len(word) > minlen:
                new_text.append(word)
        return delim.join(new_text)


    @staticmethod
    def process(text):        
        text = text.lower()
        text = Cleaner.strip_special_chars(text)
        # text = Cleaner.remove_stop_words(text)        
        return text


def read_process(filename):
    with open(filename) as reader:
        return Cleaner.process(reader.read())
        

if __name__ == "__main__":
    posdir = "./txt_sentoken/pos/"
    negdir = "./txt_sentoken/neg/"

    data = []
    # read positive in
    for posfile in os.listdir(posdir):
        data.append(('pos', read_process(posdir + posfile)))
    
    for negfile in os.listdir(negdir):
        data.append(('neg', read_process(negdir + negfile)))
    random.shuffle(data)
    with open('cleaned.csv', 'w') as writer:
        for datapoint in data:
            writer.write("{},{}\n".format(datapoint[0], datapoint[1]))
        