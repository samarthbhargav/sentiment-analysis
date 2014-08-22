# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 21:33:52 2014

@author: Samarth Bhargav
"""
from classify import BayesClassifier
from sklearn.utils import shuffle
if __name__ == "__main__":
    data=[]
    target=[]
    split = 0.6
    clf = BayesClassifier()
    clf.set_corpus([""])
    
    with open('cleaned.csv') as reader:
        for line in reader:
            datapoint = line.split(",")
            data.append(datapoint[1])
            target.append(datapoint[0])
            clf.append_to_corpus(datapoint[1])
            
    data, target = shuffle(data,target)        
    
    split = int(split * len(data))
        
    clf.train(data[:split], target[:split])
    
    correct = 0
    for x,y in zip(data[split:], target[split:]):
        if y == clf.predict(x):
            correct += 1
    print "Accuracy:",100 * float(correct) / len(data[split:])
    