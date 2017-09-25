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
        # To be implented
    # }}}
                    
    def base_entropy(self, classifier): #evaluates the base information gain, from which other values are subtracted #{{{
        classifier_values_count = {} #counts of the classification values
        classifier_values_set = set()
        information_gain=0.0
        for datum in self.data:                                             #from the values of the classifier, create a set
            classifier_values_set.add(datum.get(classifier))
        classifier_values_count = dict.fromkeys(classifier_values_set, 0)   #from the set of classifier values, create a dictionary for counting them
        for datum in self.data:
            classifier_values_count[datum.get(classifier)]+=1
        #print classifier_values_count
        for key in classifier_values_count.keys():
            temp_information_gain=0.0
            temp_information_gain_2=0.0
            temp_information_gain=float((float(classifier_values_count.get(key)))/(float(len(self.data))))
            #print temp_information_gain
            temp_information_gain_2=-math.log(temp_information_gain,2)
            #print "temp_information_gain_2"
            #print temp_information_gain_2
            temp_information_gain=temp_information_gain*temp_information_gain_2
            #print "temp_information_gain"
            #print temp_information_gain
            information_gain+=temp_information_gain
        return information_gain
    # }}}

    def entropy(self, classifier, attribute): #calculates the entropy of a particular attribute #{{{
        attribute_values_count = {} #counts of the classification values
        attribute_values_set = set()
        forest = {}
        entropy_summation=0.0
        for datum in self.data:                                             #from the values of the classifier, create a set
            attribute_values_set.add(datum.get(attribute))
        forest = dict.fromkeys(attribute_values_set)   #from the set of classifier values, create a dictionary for counting them
                                                       # DO not use the default value with objects, as it just links all things
                                                       #  in the dictionary to the same object
        attribute_values_count = dict.fromkeys(attribute_values_set, 0)   #from the set of classifier values, create a dictionary for counting them
        for tree in forest.keys():
            forest[tree]=Tree()
        #print forest.keys()
        #print forest.values()
        for datum in self.data:
            #print datum.get(attribute)
            forest[datum.get(attribute)].add_data(datum)
            attribute_values_count[datum.get(attribute)]+=1
        for tree in forest.keys():
            #forest[tree].write()
            #print forest[tree]
            #print "tree subset base entropy"
            #print forest[tree].base_entropy(classifier)
            entropy_summation+=(float(float(attribute_values_count.get(tree))/(float(len(self.data)))))*forest[tree].base_entropy(classifier)
        #print "entropy_summation"
        #print entropy_summation
        return entropy_summation
        # }}}

    def information_gain(self, classifier, attribute):
        #print "base_entropy"
        #print self.base_entropy(classifier)
        #print "summation"
        #print self.entropy(classifier, attribute)
        return (self.base_entropy(classifier) - self.entropy(classifier, attribute))

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

#my_file='altitude.csv'
my_file='photos.csv'
classifier='Class'
root = Tree()
root.file_read(my_file)
#root.choose_comparator(classifier)
root.write()
temp_classifier='Family'
information_gain=root.information_gain(temp_classifier, 'Cartoon')
print (information_gain)
#temp_classifier='Cartoon'
#information_gain-=root.entropy(temp_classifier)
#print (information_gain)
#root.file_write("output.dict")

