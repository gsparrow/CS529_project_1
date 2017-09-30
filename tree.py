#!/usr/bin/python3
# vim: expandtab softtabstop=4 shiftwidth=4 foldmethod=marker
# --------------------------------------------------------------------------------------------------
# * @file:      tree.py
# * @authors:    George Sparrow and Jenniffer Estrada  
# * @date:      
# *  Created:       Sunday, September 17, 2017
# *  Last Update:   Tuesday, September 28, 2017
# * Language:       Python
# * Course:         Machine Learning
# * Assignment:     Project 1
# * Description:    Contains the implementation of the Tree class
# --------------------------------------------------------------------------------------------------

import sys
import csv
import random
import pdb
import math

class Tree(object):
    """ Docstring Placeholder """
    def __init__(self):
        self.left = None
        self.right = None
        self.data = []
        self.headers = []
        self.chi_squared_headers = []
        self.chi_squared_data = []
        self.comparator = []

    def file_read(self, filename, header): #{{{
        """ Docstring Placeholder """
        with open(filename) as csvfile:
            if (header == 1):
                reader = csv.DictReader(csvfile)
            else:
                reader = csv.DictReader(csvfile, fieldnames=("ID","Sequence","Class"))
            self.headers = reader.fieldnames
            for row in reader:
                self.data.append(row)
    # }}}

    def chi_squared_read(self, filename): #{{{
        """ Docstring Placeholder """
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            self.chi_squared_headers = reader.fieldnames
            for row in reader:
                self.chi_squared_data.append(row)
        for row in self.chi_squared_data:
            for column in row:
                row[column] = float(row.get(column))
    # }}}

    # Write File Output functions {{{
    def file_write_inorder(self, filename):
        """ Docstring Placeholder """
        if (self.left):
            self.left.write()
        with open(filename, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            writer.writeheader()
            for datum in self.data:
                writer.writerow(datum)
            csvfile.write( "\n" )
        if (self.right):
            self.right.write()

    def file_write_preorder(self, filename):
        """ Docstring Placeholder """
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
        """ Docstring Placeholder """
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
        """ Docstring Placeholder """
        self.file_write_inorder(filename)
    # }}}

    # Write stdout Output functions {{{
    def write_inorder(self):
        """ Docstring Placeholder """
        if (self.left):
            self.left.write()
        sys.stdout.write(str(self.comparator) + "\n")
        for datum in self.data:
            sys.stdout.write(str(datum) + "\n")
        print
        if (self.right):
            self.right.write()

    def write_preorder(self):
        """ Docstring Placeholder """
        for datum in self.data:
            sys.stdout.write(str(datum) + "\n")
        print
        if (self.left):
            self.left.write()
        if (self.right):
            self.right.write()

    def write_postorder(self):
        """ Docstring Placeholder """
        if (self.left):
            self.left.write()
        if (self.right):
            self.right.write()
        for datum in self.data:
            sys.stdout.write(str(datum) + "\n")
        print

    def write(self):
        """ Docstring Placeholder """
        self.write_inorder()
    # }}}

    def add_data(self, datum): #{{{
        """ Docstring Placeholder """
        self.data.append(datum)
    # }}}

    def compute_max_information_gain(self, classifier): #{{{
        """ Docstring Placeholder """
        entropy_dictionary = {}
        max_information_gain = 0.0
        if (self.data):
            temp_attribute_list = self.data[0].keys()
            temp_attribute_list.remove(classifier)
            entropy_dictionary = dict.fromkeys(temp_attribute_list, 0.0)
            #print entropy_dictionary
            for attribute in entropy_dictionary.keys():
                entropy_dictionary[attribute]=self.information_gain(classifier, attribute)
            #print entropy_dictionary
            max_information_gain = max(entropy_dictionary.values())
            #print max_information_gain
            for pair in entropy_dictionary.items():
                if (pair[1] == max_information_gain):
                    pair_to_return = pair
            #print pair_to_return
            return pair_to_return[0] #returns just the attribute
        else:
            print "I have no data to compute the max information gain from"
            exit(1)
    # }}}

    def base_entropy(self, classifier): #evaluates the base information gain, from which other values are subtracted #{{{
        """ Docstring Placeholder """
        classifier_values_count = {} #counts of the classification values
        classifier_values_set = set()
        information_gain=0.0
        for datum in self.data:                                             #from the values of the classifier, create a set
            classifier_values_set.add(datum.get(classifier))
        classifier_values_count = dict.fromkeys(classifier_values_set, 0)   #from the set of classifier values, create a dictionary for counting them
        for datum in self.data:
            classifier_values_count[datum.get(classifier)] += 1
        #print classifier_values_count
        for key in classifier_values_count.keys():
            temp_information_gain = 0.0
            temp_information_gain_2 = 0.0
            temp_information_gain = float((float(classifier_values_count.get(key)))/(float(len(self.data))))
            #print temp_information_gain
            temp_information_gain_2 = -math.log(temp_information_gain,2)
            #print "temp_information_gain_2"
            #print temp_information_gain_2
            temp_information_gain = temp_information_gain*temp_information_gain_2
            #print "temp_information_gain"
            #print temp_information_gain
            information_gain += temp_information_gain
        return information_gain
    # }}}

    def entropy(self, classifier, attribute): #calculates the entropy of a particular attribute #{{{
        """ Docstring Placeholder """
        attribute_values_count = {} #counts of the classification values
        attribute_values_set = set()
        forest = {}
        entropy_summation = 0.0
        for datum in self.data:                                             #from the values of the classifier, create a set
            attribute_values_set.add(datum.get(attribute))
        forest = dict.fromkeys(attribute_values_set)   #from the set of classifier values, create a dictionary for counting them
                                                       # DO not use the default value with objects, as it just links all things
                                                       #  in the dictionary to the same object
        attribute_values_count = dict.fromkeys(attribute_values_set, 0)   #from the set of classifier values, create a dictionary for counting them
        for tree in forest.keys():
            forest[tree] = Tree()
        #print forest.keys()
        #print forest.values()
        for datum in self.data:
            #print datum.get(attribute)
            forest[datum.get(attribute)].add_data(datum)
            attribute_values_count[datum.get(attribute)] += 1
        for tree in forest.keys():
            #forest[tree].write()
            #print forest[tree]
            #print "tree subset base entropy"
            #print forest[tree].base_entropy(classifier)
            entropy_summation += (float(float(attribute_values_count.get(tree))/(float(len(self.data)))))*forest[tree].base_entropy(classifier)
        #print "entropy_summation"
        #print entropy_summation
        return entropy_summation
        #}}}

    def information_gain(self, classifier, attribute): # #{{{
        """ Docstring Placeholder """
        #print "base_entropy"
        #print self.base_entropy(classifier)
        #print "summation"
        #print self.entropy(classifier, attribute)
        return self.base_entropy(classifier) - self.entropy(classifier, attribute)
         #}}}

    def chi_squared(self, attribute, probability): #{{{
        """ Docstring Placeholder """
        attribute_values_count = {} #counts of the attribute values
        attribute_values_set = set() #holds both the degrees of freedom, and helps calculate the expected value
        degrees_of_freedom = 0
        expected_value = 0.0
        critical_value = 0.0 #from the chi_squared csv
        temp_value = 0.0
        chi_squared_value = 0.0
        for datum in self.data:
            attribute_values_set.add(datum.get(attribute))
        attribute_values_count = dict.fromkeys(attribute_values_set, 0)
        #print attribute_values_set
        for datum in self.data:
            attribute_values_count[datum.get(attribute)] += 1
        degrees_of_freedom = ((len(attribute_values_set))-1)
        #print degrees_of_freedom
        expected_value = float(float(len(self.data))/float(len(attribute_values_set)))
        #print expected_value
        for key in attribute_values_count.keys():
            temp_value = float(expected_value) - float(attribute_values_count.get(key))
            #print "Expected value"
            #print expected_value
            #print "actual value"
            #print float(attribute_values_count.get(key))
            #print "Temp value"
            #print temp_value
            temp_value = float(temp_value * temp_value)
            #print "Temp value"
            #print temp_value
            temp_value = float(temp_value/expected_value)
            #print "Temp value"
            #print temp_value
            chi_squared_value += temp_value
        degrees_fo_freedom = 20
        critical_value = self.chi_squared_data[(degrees_of_freedom-1)].get(probability)
        print critical_value
        print chi_squared_value
        if (critical_value >= chi_squared_value):
            return True #Null hypothesis is correct
        else:
            return False #Null hypothesis is rejected
    #}}}

    def choose_comparator(self, classifier): #{{{
        """ Docstring Placeholder """
        same = True
        temp_headers = []
        classifier_values_set = set()
        for datum in self.data:
            classifier_values_set.add(datum.get(classifier))
        if (self.data):
            for datum in self.data:
                classifier_values_set.add(datum.get(classifier))
            if (len(classifier_values_set) == 1):
                self.comparator = int(self.data[0].get(classifier))
                return
            else:
                self.comparator = self.compute_max_information_gain(classifier) #this will compute the information gain and use its attribute as its comparator
                #print str(self.compute_max_information_gain(classifier))
                #temp_headers=self.data[0].keys()
                #temp_headers.remove(classifier)
                #self.comparator=random.choice(temp_headers) #this is what chooses the comparator of the node, in this case psuedorandomness
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

    def base_gini_index(self, classifier): # Evaluates the system gini index #{{{
        """ Docstring Placeholder """
        classifier_values_count = {} # Counts of the classification values
        classifier_values_set = set()
        system_gini_value = 0.0
        for datum in self.data:                                             # From the values of the classifier, create a set
            classifier_values_set.add(datum.get(classifier))
        classifier_values_count = dict.fromkeys(classifier_values_set, 0)   # From the set of classifier values, create a dictionary for counting them
        for datum in self.data:
            classifier_values_count[datum.get(classifier)] += 1
        for key in classifier_values_count.keys():
            temp_gini_value = 0.0
            temp_system_value = 0.0
            temp_system_value = float((float(classifier_values_count.get(key)))/(float(len(self.data))))
            temp_gini_value += float(float(temp_system_value) ** float(2.0))
        system_gini_value = float(float(1.0) - float(temp_gini_value))
        return system_gini_value
    # }}}

    def attribute_impurity(self, classifier, attribute): # Calculates the gini index value for a particular attribute #{{{
        """ Calculates the Gini Index for an attribute """
        attribute_values_count = {} # Counts of the classification values
        attribute_values_set = set()
        attr_class_values_count = {} # Counts of the class values
        attr_class_values_set = set()
        forest = {}
        gini_summation = 0.0
        for datum in self.data:                                             # From the values of the classifier, create a set
            attribute_values_set.add(datum.get(attribute))
            attr_class_values_set.add(datum.get(classifier))
        print "Attribute value set"
        print attribute_values_set
        print "class Attribute value set"
        print attr_class_values_set

        attribute_values_count = dict.fromkeys(attribute_values_set, 0)   # From the set of classifier values, create a dictionary for counting them
        attr_class_values_count = dict.fromkeys(attr_class_values_set, 0)   # From the set of classifier values, create a dictionary for counting them
        for datum in self.data:
            attribute_values_count[datum.get(attribute)] += 1
            attr_class_values_count[datum.get(classifier)] += 1
        print "Attribute value counts"
        print attribute_values_count
        print "class Attribute value counts"
        print attr_class_values_count
        print "length of data"
        print float(len(self.data))
        temp_gini_index = 0.0
        for key in attribute_values_count.keys():
            temp_gini_index += float(((float(attr_class_values_count.get(key)))/(float(len(self.data)))))**2.0
            gini_summation = temp_gini_index
        gini_index = 1-gini_summation
        print gini_index
        return gini_index
        # }}}

    def predict(self, classifier, datum): #Predicts the classifier of a datum {{{
        if (self.left):
            if (int(datum.get(self.comparator)) == 1):
                return self.left.predict(datum)
            else:
                return self.right.predict(datum)
        else:
            classifier_values_count = {} #counts of the classification values
            classifier_values_set = set()
            data_value =0
            for datum in self.data:                                             #from the values of the classifier, create a set
                classifier_values_set.add(datum.get(classifier))
            classifier_values_count = dict.fromkeys(classifier_values_set, 0)   #from the set of classifier values, create a dictionary for counting them
            for datum in self.data:
                classifier_values_count[datum.get(classifier)] += 1
            for key in classifier_values_set.keys():
                if (classifier_values_set.get(key) > data_value):
                    data_value = classifier_values_set.get(key)
                    data_attribute = key
            return data_value
    # }}}
                
        

def main(): # Main function call #{{{
    """ Main Function call for testing Tree class"""
    #my_file='altitude.csv'
    header = 0 # Turn this option on if there is a header in the csv being read!!!!
    my_file='training.csv'
    #chi_squared_file='chisquared.csv'
    #my_file='photos.csv'
    #classifier='Class'
    #PROBABILITY='0.050'
    #root = Tree()
    #root.file_read(my_file)
    #root.chi_squared_read(chi_squared_file)
    #print root.chi_squared_headers
    #print root.chi_squared_data
    #root.choose_comparator(classifier)
    #root.write()
    #print root.chi_squared(classifier, PROBABILITY)
    #temp_classifier='Family'
    #print root.compute_max_information_gain(temp_classifier)
    #information_gain=root.information_gain(temp_classifier, 'Cartoon')
    #print (information_gain)
    #temp_classifier='Cartoon'
    #information_gain-=root.entropy(temp_classifier)
    #print (information_gain)
    #root.file_write("output.dict")
    #my_file='altitude.csv'
    #my_file = 'photos.csv'
    #classifier='Family'
    root = Tree()
    root.file_read(my_file, header)
    #root.choose_comparator(classifier)
    #root.write()
    #temp_classifier = 'Family'
    class_label = 'Class'
    attribute = 'Sequence'
    #print root.compute_max_information_gain(classifier)
    #print information_gain=root.information_gain(classifier, attribute)
    #print (information_gain)
    #temp_classifier='Cartoon'
    #information_gain-=root.entropy(temp_classifier)
    #print (information_gain)
    #root.file_write("output.dict")
    print '========================================'
    print root.base_gini_index(class_label)
    print '========================================'
    print root.attribute_impurity(class_label, attribute)

if __name__ == "__main__":
    main()

    #}}}
