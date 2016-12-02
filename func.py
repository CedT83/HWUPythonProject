#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

################################## Imports
#We use matplotlib to draw diagram
import matplotlib.pyplot as plt
#We use pandas to manipulate our data
import pandas as pd
#countryutils is a third-party library used to get the continent of a given country
from libraries.countryutils import transformations
#user_agents is used to parse the user_agent string easily
from libraries.user_agents import parse
#To use JSON methods we need the json module
import json
#We need to instantiate an ordered dictionary in one of our functions
from collections import OrderedDict
#We need this module to call the exit function in case we have an error and must quit the program
import sys

################################## Imports
#we need this otherwise pandas will not work here
good_columns = ['ts', 'visitor_uuid', 'visitor_username', 'visitor_source', 'visitor_device', 'visitor_useragent', 'visitor_ip', 'visitor_country', 'visitor_referrer', 'env_type', 'env_doc_id', 'env_adid', 'event_type', 'event_readtime', 'subject_type', 'subject_doc_id', 'subject_page', 'cause']

################################## Functions

#For a given stream, we retrieve a ductionary where the key is from sub-data keyElement in the stream and valueElement will be the sub-data considered as the value
#Dictionnary contains some filters we want to apply to the data
def getFor(stream, dictionary, keyElement, valueElement=1 ):
	#Here our stream is a file, we read it line per line to not use too much memory and perform actions line per line (JSON object per JSON object)
	try:
		with open(stream) as data:
			#create the dict used for the results
			elements = dict()
			#For each line 
			for line in data:
				#we consider the line as valid 
				valid = True
				#loads a JSON object into loaded_line
				try:
					loaded_line = json.loads(line)
				#If we have an exception, we go to the next line (next value in the for loop)
				except Exception:
					print("There is a non-JSON object line, we skip it")
					continue
				#we filter loaded_line using the dictionnary key:value => sub-data in loaded_line : desired value
				for k in dictionary:
					#if we don't have what we want ''
					if k not in loaded_line or loaded_line[k] not in dictionary[k] :
						#we consider the line as invalid
						valid = False
				#if the line is valid
				if valid == True :
					try:
						#we try to store the desired sub-data into the dict
						key = keyElement(loaded_line)
						#we define what we use as value for the dict
						counter = valueElement(loaded_line) if valueElement != 1 else 1
						#if key is not None:
						#if key is not in our dict we add it
						if key not in elements:
							elements[key] = counter
						#if key is already in, we add the current value to the old value
						else:
							elements[key] += counter
					#in case of invalid key we catch the exception
					except KeyError:
						#we do nothing because the data is considered as invalid
						#nothing more to do so
						pass
				#if the data is invalid wo end up here
				else:
					#we do nothing because the data is invalid
					pass
	except Exception:
		print("Specified file or default file: %s cannot be opened" % stream)
		sys.exit(-1)
	#we return the dict
	return elements

#just a simple wrapper for the method that returns the continent of the given country in CCA2 style
def getContinentWithCca2(country):
	return transformations.cca_to_ctn(country)

#we collect the data that matches a given doc_id from the stream
#this function is only used when pandas is used
def getDataForDoc(stream):
	#we open the stream
	with open(stream) as data:
		elements = list()
		#we have a LJSOn (line json file)
		#so we load json objects line per line
		for line in data:
			loaded_line = json.loads(line, object_pairs_hook=OrderedDict)
			list_line = pd.Series(loaded_line)
			#we create a list of JSON objects
			elements.append(list_line)
	#we return the list
	return elements

#for a given doc_uuid we get the browsers used to access to it
def getBrowsersForDoc(**kwargs):
	#we retrieve the name of the stream if defined
	filename = kwargs.get('filename', None)
	#we define what will be used as key in our dict
	g = lambda x : parse(x["visitor_useragent"]).browser.family
	#we define a dictionary that contains the filters we will apply on our JSON objects
	dictionary = {"event_type" : "read"}
	#if filename not defined we use a default value
	if not filename :
		filename = 'issuu.json'
	#we retrieve our data
	return getFor(filename, dictionary, g)

#for a given doc_uuid we get the countries from where people accessed it
def getCountriesForDoc(doc_uuid, **kwargs):
	#we retrieve the value to know if pandas will be used
	method = kwargs.get('method', None)
	#we retrieve the name of the stream if defined
	filename = kwargs.get('filename', None)
	#if filename not defined we use a default value
	if not filename :
		filename = 'issuu.json'
	#if pandas not activated
	if not method:
		#we define what will be used as key in our dict
		f = lambda x : x["visitor_country"]
		#we define a dictionary that contains the filters we will apply on our JSON objects
		dictionary = {"event_type" : "read", "subject_doc_id" : doc_uuid}
		#we retrieve our data
		return getFor(filename, dictionary, f)
	#pandas activated
	else:
		#we get our data in a list
		data = getDataForDoc(filename)
		#we transform our data into a pandas DataFrame
		dataFrame = pd.DataFrame(data, columns=good_columns)
		#we select the data we want
		dataFrame = dataFrame.query('subject_doc_id == @doc_uuid')
		dataFrame = dataFrame['visitor_country'].value_counts()
		#We return the dictionary with the results
		return dict(dataFrame.sort_values(ascending=False))

#for a given doc_uuid we get the continent from where people accessed it
def getContinentsForDoc(doc_uuid, **kwargs):
	#we retrieve all the countries where people accessed the document
	countries = getCountriesForDoc(doc_uuid, **kwargs)
	continents = dict()
	#for each country
	for country in countries:
		#we get its continent
		temp = getContinentWithCca2(country)
		#if not in our dict we add it
		if temp not in continents:
			#we count the number of occurences
			continents[temp] = countries[country]
		#if in the dict
		else:
			#we update the occurences
			continents[temp] += countries[country]
	#we return the results
	return continents

#for a given doc_uuid we get the users that accessed it
def getUsersForDoc(doc_uuid, **kwargs):
	#we retrieve the name of the stream if defined
	filename = kwargs.get('filename', None)
	#we define what will be used as key in our dict
	f = lambda x : x["visitor_uuid"]
	#we define a dictionary that contains the filters we will apply on our JSON objects
	dictionary = {"event_type" : "read", "subject_doc_id" : doc_uuid}
	#if filename not defined we use a default value
	if not filename:
		filename = 'issuu.json'
	#we return the results
	return list(getFor(filename, dictionary, f).keys())

#for a given user_uuid we determine which documents he has read
def getDocsForUser(user_uuid, **kwargs):
	#we retrieve the name of the stream if defined
	filename = kwargs.get('filename', None)
	#we define what will be used as key in our dict
	f = lambda x : x["subject_doc_id"]
	#we define a dictionary that contains the filters we will apply on our JSON objects
	dictionary = {"event_type" : "read", "visitor_uuid" : user_uuid}
	#if filename not defined we use a default value
	if not filename:
		filename = 'issuu.json'
	#we return the results
	return list(getFor(filename, dictionary, f).keys())

def getReadership(size=None, **kwargs):
	#we retrieve the name of the stream if defined
	filename = kwargs.get('filename', None)
	#we define what will be used as key in our dict
	f = lambda x : x["visitor_uuid"]
	#we define what will be used as value in our dict
	y = lambda x : x["event_readtime"]
	#we define a dictionary that contains the filters we will apply on our JSON objects
	dictio = {}
	#We will need an orderedDict to store the results. All our functions returns Dict so we need a dict, but an ordered one
	result = OrderedDict()
	#if filename not defined we use a default value
	if not filename:
		filename = 'issuu.json'
	#we get the data
	data = getFor(filename, dictio, f, y)
	#we sort the data.keys using the value (time spent on reading) and keep the 10 firsts
	temp = sorted(data, key=data.get, reverse=True)[:size]
	if size != None:
		temp = temp[:size]
	#for each element in the sorted liste above we create a dict using the element as key and its value in data as value for the orderedDict
	for i in temp:
		result[i] = data[i]
	#we return the results (the orderedDict)
	return result

#a simple function that counts the number of occurences in a list and creates tuples
def cleanup(someList):
	l = []
	for i in someList:
		m = someList.count(i)
		l.append((i, m))
	return remove_adjacent(l)

#A simple function that removes multiple elements in a list
def remove_adjacent(someList):
	l = []
	#for each element in the list
	for i in someList:
		#if the element is not in the new list we add it
		if i not in l:
			l.append(i)
	#we return the new list containing unique elements
	return l

def show_histo(variable, orient="horiz", label="counts", title="title"):
	if  not isinstance(variable, dict):
		return
	"""Take a dictionary of counts and show it as a histogram."""
	if orient=="horiz":    # NB: this assigns a function to bar_fun!
		bar_fun = plt.barh; bar_ticks = plt.yticks; bar_label = plt.xlabel
	elif orient=="vert":
		bar_fun = plt.bar; bar_ticks = plt.xticks ; bar_label = plt.ylabel
	else:
		raise Exception("show_histo: Unknown orientation: %s ".format % orient)
	n = len(variable)
	bar_fun(range(n), list(variable.values()), align='center', alpha=0.4)
	bar_ticks(range(n), list(variable.keys()))  # NB: uses a higher-order function
	bar_label(label)
	plt.title(title)
	plt.show()
