#!/usr/bin/python3
# vim: expandtab softtabstop=4 shiftwidth=4 foldmethod=marker
import sys
import csv
import random
import pdb
import math

class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data=[]
        self.headers=[]
        self.comparator=[]

    def file_read(self, filename):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            self.headers=reader.fieldnames
            for row in reader:
                self.data.append(row)

    # Write File Output functions {{{
    def file_write_inorder(self, filename):
        if (self.left):
            self.left.write()
        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            for datum in self.data:
                writer.writerow(datum)
            csvfile.write("\n" )
        if (self.right):
            self.right.write()

    def file_write_preorder(self, filename):
        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            for datum in self.data:
                writer.writerow(datum)
            csvfile.write("\n" )
        if (self.left):
            self.left.write()
        if (self.right):
            self.right.write()

    def file_write_postorder(self, filename):
        if (self.left):
            self.left.write()
        if (self.right):
            self.right.write()
        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            for datum in self.data:
                writer.writerow(datum)
            csvfile.write("\n" )

    def file_write(self, filename):
        self.file_write_inorder(filename)
    # }}}

    # Write stdout Output functions {{{
    def write_inorder(self):
        if (self.left):
            self.left.write()
        sys.stdout.write(str(self.comparator) + "\n")
        for datum in self.data:
            sys.stdout.write(str(datum) + "\n")
        print
        if (self.right):
            self.right.write()

    def write_preorder(self):
        for datum in self.data:
            sys.stdout.write(str(datum) + "\n")
        print
        if (self.left):
            self.left.write()
        if (self.right):
            self.right.write()

    def write_postorder(self):
        if (self.left):
            self.left.write()
        if (self.right):
            self.right.write()
        for datum in self.data:
            sys.stdout.write(str(datum) + "\n")
        print

    def write(self):
        self.write_inorder()
    # }}}

    def add_data(self, datum):
        self.data.append(datum)

    def compute_max_information_gain(self, classifier): #{{{
        information_gains=[]
        temp_values=set()
        temp_pairs={}
        if (self.data):
            for key in self.data[0].keys(): # for each of the different keys
                temp_pairs={}
                for iterator in range(0, len(self.data)): #for each of the datum in data
                    if (self.data[iterator].get(key)): #if the datum exists
                        if (temp_pairs.get(self.data[iterator].get(key))): #if the value exists as a key-value pair in temp_pairs
                            temp_pairs[self.data[iterator].get(key)]+=1.0
                        else:
                            temp_pairs[self.data[iterator].get(key)]=1.0 #if the value DNE as a key-value pair in temp_pairs
                print str(temp_pairs)   #verbose
                for iterator in range(0, len(temp_pairs.keys())-1): #now that we have a list of the totals of values
                    if (iterator==0):
                        information_gains.append(-math.log(float    #summation for entropy, -log(value_subset/set)
                                                            (float(temp_pairs.get(temp_pairs.keys()[iterator])))
                                                            /float(len(self.data))))
                    else:
                        information_gains[iterator]-=math.log(float
                                                            (float(temp_pairs.get(temp_pairs.keys()[iterator])))
                                                            /float(len(self.data)))
            print str(information_gains)    #verbose
            for iterator in range(0, len(information_gains)):   #return where the key is for the max information gain
                if (information_gains[iterator] == (float(max(information_gains)))):
                    return iterator
        else:
            print "There was an error and this node has no data"
            exit()
    # }}}
                    
    def base_information_gain(self, classifier):
        classifier_values_count = {} #counts of the classification values
        classifier_values_set = set()
        for datum in self.data:                                             #from the values of the classifier, create a set
            classifier_values_set.add(datum.get(classifier))
        classifier_values_count = dict.fromkeys(classifier_values_set, 0)   #from the set of classifier values, create a dictionary for counting them
        information_gain=0.0
        for datum in self.data:
            classifier_values_count[classifier]+=1
        for key in classifier_values_count.keys():
            information_gain-=(float(float(classification_values_count.get(key))/len(self.data)))*math.log(float(float(classification_values_count.get(key))/len(self.data)))
        return information_gain

    def choose_comparator(self, classifier): #{{{
        same=True
        temp_headers=[]
        classifier_values_set = set()
        for datum in self.data:
            classifier_values_set.add(datum.get(classifier))
        if (self.data):
            for datum in self.data:
                classifier_values_set.add(datum.get(classifier))
            if (len(classifier_values_set) ==1):
                self.comparator=int(self.data[0].get(classifier))
                return
            else:
                #self.comparator=self.compute_max_information_gain(classifier) #this will compute the information gain and use it as its comparator
                #print str(self.compute_max_information_gain(classifier))
                temp_headers=self.data[0].keys()
                temp_headers.remove(classifier)
                self.comparator=random.choice(temp_headers) #this is what chooses the comparator of the node, in this case psuedorandomness
                self.left = Tree()
                self.right = Tree()
                while (self.data):
                    if (int(self.data[0].get(self.comparator)) == 1): #this assumes a binary value
                        self.left.add_data(self.data[0])
                        self.data.remove(self.data[0])
                    else:
                        self.right.add_data(self.data[0])
                        self.data.remove(self.data[0])
                self.left.choose_comparator(classifier)
                self.right.choose_comparator(classifier)
        else: #an error has occured, there is no data in this leaf
            return
    # }}}

my_file='altitude.csv'
classifier='Class'
root = Tree()
root.file_read(my_file)
root.choose_comparator(classifier)
root.write()
#root.file_write("output.dict")

