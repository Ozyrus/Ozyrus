#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import division
import time
from lxml import etree as ET
#import xml.etree.ElementTree as ET
import csv
from pymystem3 import Mystem
import codecs
import subprocess
import re
import math
import random
import curses.ascii
firstxelem = 1000
ThemesQuantitymanual = {}
ThemesQuantity ={'Технологии|Физика|Наука и технологии|Биология|Медицина|Компьютерные технологии': 378, 'Преступность и право': 13, 'В мире': 271, 'Культура': 283, 'Экзотика': 66, 'Интернет': 29, 'Здоровье': 141, 'Спорт|Шахматы|Футбол|Хоккей|Формула 1': 82, 'Происшествия': 34, 'Книги': 56, 'Материалы VOA News|Материалы Lenta.ru|Материалы РИА Новости|Материалы BBC|Переведенные новости': 82, 'Медиа': 225, 'Космонавтика|материалы NASA|МКС|Астрономия|NASA': 72, 'Общество': 386, 'Политика|Политика США': 107, 'Экономика': 233}
def lex_count(lexemes):
	d_lex = {}
	#здесь должен быть массив с очищенными словами. каждый элемент - чистое слово без всякое хуйни
	for lex in lexemes:
		if lex not in d_lex:
			d_lex[lex] = 1
		else:
			d_lex[lex] += 1
	d_lex = dict(sorted(d_lex.items(), key=lambda x: x[1], reverse=True))
	# for k, v in sorted(d_lex.items(), key=lambda x: x[1], reverse=True):
	# 	fout.write(k + ';' + str(v))
	# 	fout.write('\r\n')
	# 	fout.write(u'Всего слов в параметре lex: '+ str(len(lexemes)))
	Totalsum = 0
	for k, v in d_lex.iteritems():
		Totalsum +=v
	Listofprobabilities= []
	Listofkeys = []
	for k, v in d_lex.iteritems():
		Listofkeys.append(k)
		Probability = int(v) / float(Totalsum)
		Listofprobabilities.append(Probability)
	SortedProbabilityDictionary = dict(zip(Listofkeys,Listofprobabilities))
	print type(SortedProbabilityDictionary)
	return SortedProbabilityDictionary
def ifdoctxt(file):
	text = codecs.open('testtext.txt', 'r')
	string = str(text.read())
	return string
def ifdocxmlGRAM(file):
	root = ET.parse(file)
	massive=[]
	for atype in root.findall("./text/paragraphs/paragraph/sentence/tokens/token/tfr/v[1]/l[1]/g[1]"):
		x = atype.get('v')
		massive.append(x)
	return massive
def ifdocxmlWORDS(file):
	root = ET.parse(file)
	massive=[]
	for atype in root.findall("./text/paragraphs/paragraph/sentence/tokens/token/tfr/v[1]/l[1]"):
		x = atype.get('t')
		x = x.encode('utf-8')
		if re.match('[^«»][А-Яа-яA-Za-zё]+', x):	
			#print x
			massive.append(x)
	return massive
def ifdocxmlBIGRAM(file):
	root = ET.parse(file)
	massive=[]
	for atype in root.findall("./text/paragraphs/paragraph/sentence/tokens/token/tfr/v/l"):
		massiveinner=[]
		print atype.get('t').encode('utf-8')
		massiveinner.append(atype.get('t'))
		for i in range(len(massiveinner)-1):
			massive.append(a[i]+' '+a[i+1])
	for i in massive:
		print i
	return massive
def wordListToFreqDict(wordlist):
	wordfreq = [wordlist.count(p) for p in wordlist]
	b=sum(wordfreq)
	perem = zip(wordlist,wordfreq)
	perem = list(set(perem))
	return perem
def sortFreqDict(freqdict):
	aux = sorted(freqdict,key=(lambda item: item[1]), reverse=True)
	aux = aux[:firstxelem]
	aux = sorted(aux,key=lambda item: item[0])
	return aux
def sortFreqDictNice(freqdict):
	aux = sorted(freqdict,key=(lambda item: item[0]))
	aux = aux[:firstxelem]
	aux = sorted(aux,key=lambda item: item[1], reverse=True)
	return aux
def Texttolemmafreq(string):
	m = Mystem()
	lemmassive = m.lemmatize(string)
	Dictionary = wordListToFreqDict(lemmassive)
	SortedDictionary = sortFreqDict(Dictionary)
	with open('freqdictionarywords.csv','w') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['Token','Number'])
	    for row in SortedDictionary:
	        csv_out.writerow(row)
def Texttogramfreq(string):
	mycommandline = ["mystem","-clingd", "--format", "xml","--eng-gr", "testtext.txt","output.xml"]
	subprocess.call(mycommandline)
	root = ET.parse('output.xml')
	massive=[]
	massive2=[]
	for atype in root.findall(".//ana"):
		massive.append(atype.get('gr'))
	for i in massive:
		a = i.split(',')[0].split('=')[0]
		print a
		massive2.append(a)
	Dictionary = wordListToFreqDict(massive2)
	SortedDictionary = sortFreqDict(Dictionary)
	with open('freqdictionarygramTXT.csv','w') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['Token','Number'])
	    for row in SortedDictionary:
	        csv_out.writerow(row)
def XMLtowordfreq(string):
	Dictionary = wordListToFreqDict(string)
	SortedDictionary = sortFreqDict(Dictionary)
	with open('freqdictionaryXMLWORDS.csv','w') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['Token','Number'])
	    for row in SortedDictionary:
	    	row = list(row)
	    	row[0]=row[0].encode('utf-8')	    	
	        csv_out.writerow(row)
	Totalsum = 0
	SortedDictionary = dict(SortedDictionary)
	for k, v in SortedDictionary.iteritems():
		Totalsum +=v
	Listofprobabilities= []
	Listofkeys = []
	for k, v in SortedDictionary.iteritems():
		Listofkeys.append(k)
		Probability = int(v) / float(Totalsum)
		Listofprobabilities.append(Probability)
	SortedProbabilityDictionary = dict(zip(Listofkeys,Listofprobabilities))
	print type(SortedProbabilityDictionary)
	return SortedProbabilityDictionary
def XMLtogramfreq(string):
	Dictionary = wordListToFreqDict(string)
	SortedDictionary = sortFreqDict(Dictionary)
	with open('freqdictionarygram.csv','w') as out:
	    csv_out=csv.writer(out)
	    csv_out.writerow(['Token','Number'])
	    for row in SortedDictionary:
	    	row = list(row)
	    	row[0]=row[0].encode('utf-8')	
	        csv_out.writerow(row)
	Totalsum = 0
	SortedDictionary = dict(SortedDictionary)
	for k, v in SortedDictionary.iteritems():
		Totalsum +=v
	Listofprobabilities= []
	Listofkeys = []
	for k, v in SortedDictionary.iteritems():
		Listofkeys.append(k)
		Probability = int(v) / float(Totalsum)
		Listofprobabilities.append(Probability)
	SortedProbabilityDictionary = dict(zip(Listofkeys,Listofprobabilities))
	print type(SortedProbabilityDictionary)
	return SortedProbabilityDictionary
def countthemes(string): #lets first count how many of different themes we have in corpus and output the percentage
	root = ET.parse(string)
	massive = []
	tema = 'Тема:(.+:.+)'
	tip = 'Тип:(.+)'
	for atype in root.findall("./text/tags/tag"):
		x = atype.text.encode('utf-8')
		Biba2 = re.search(tema, x)
		if Biba2:
			Biba = Biba2.group(1)
			print Biba
			massive.append(Biba)
	wordfreq = [massive.count(p) for p in massive]
	sumoftexts = sum(wordfreq)
	print 'Out of',sumoftexts,' texts there are '
	brabus = sortFreqDictNice(wordListToFreqDict(massive))
	for item in brabus:
		print str(item[0]) + ',' + str(item[1])
def defthemescorpus():
	Corpus_text_amount = 0
	ThemesQuantitymanual ={}
	Obschestvo = input('Please enter amount of text with theme Obschestvo; total amount of texts with this theme is 328 out of 1974: ')
	ThemesQuantitymanual['Общество']= Obschestvo
	Corpus_text_amount += Obschestvo
	Cultura = input('Please enter amount of text with theme Cultura; total amount of texts with this theme is 250 out of 1974: ')
	Corpus_text_amount += Cultura
	ThemesQuantitymanual['Культура']= Cultura
	V_mire = input('Please enter amount of text with theme V_mire; total amount of texts with this theme is 213 out of 1974: ')
	Corpus_text_amount += V_mire
	ThemesQuantitymanual['В мире']= V_mire
	Technology = input('Please enter amount of text with theme Technology; total amount of texts with this theme is 298 out of 1974: ')
	Corpus_text_amount += Technology
	ThemesQuantitymanual['Технологии|Физика|Наука и технологии|Биология|Медицина|Компьютерные технологии']= Technology # Физика+ Наука и технологии + Биология + Медицина +Компьютерные технологии
	Economica = input('Please enter amount of text with theme Economica; total amount of texts with this theme is 202 out of 1974: ')
	Corpus_text_amount += Economica
	ThemesQuantitymanual['Экономика']= Economica
	Media = input('Please enter amount of text with theme Media; total amount of texts with this theme is 194 out of 1974: ')
	Corpus_text_amount += Media
	ThemesQuantitymanual['Медиа']= Media
	Zdorovie = input('Please enter amount of text with theme Zdorovie; total amount of texts with this theme is 100 out of 1974: ')
	Corpus_text_amount += Zdorovie
	ThemesQuantitymanual['Здоровье']= Zdorovie
	Politica = input('Please enter amount of text with theme Politica; total amount of texts with this theme is 93 out of 1974: ')
	Corpus_text_amount += Politica
	ThemesQuantitymanual['Политика|Политика США']= Politica	# + Политика США
	Exotica = input('Please enter amount of text with theme Exotica; total amount of texts with this theme is 50 out of 1974: ')
	Corpus_text_amount += Exotica
	ThemesQuantitymanual['Экзотика']= Exotica
	Knigi = input('Please enter amount of text with theme Knigi; total amount of texts with this theme is 50 out of 1974: ')
	Corpus_text_amount +=Knigi
	ThemesQuantitymanual['Книги']= Knigi
	Sport = input('Please enter amount of text with theme Sport; total amount of texts with this theme is 50 out of 1974: ')
	Corpus_text_amount +=Sport
	ThemesQuantitymanual['Спорт|Шахматы|Футбол|Хоккей|Формула 1']= Sport # +Шамхаты + Футбол + Хоккей + Формула 1
	Novosti = input('Please enter amount of text with theme Novosti; total amount of texts with this theme is 43 out of 1974: ')
	Corpus_text_amount +=Novosti
	ThemesQuantitymanual['Материалы VOA News|Материалы Lenta.ru|Материалы РИА Новости|Материалы BBC|Переведенные новости']= Novosti # атериалы VOA News + Материалы Lenta.ru + Материалы РИА Новости + Материалы BBC + Переведенные новости
	Cosmonautica = input('Please enter amount of text with theme Cosmonautica; total amount of texts with this theme is 50 out of 1974: ')
	Corpus_text_amount += Cosmonautica
	ThemesQuantitymanual['Космонавтика|Материалы NASA|МКС|Астрономия|NASA']= Cosmonautica # +материалы NASA +МКС + Астрономия + NASA
	Proishestviya = input('Please enter amount of text with theme Proishestviya; total amount of texts with this theme is 23 out of 1974: ')
	Corpus_text_amount +=Proishestviya
	ThemesQuantitymanual['Происшествия']= Proishestviya
	Internet = input('Please enter amount of text with theme Internet; total amount of texts with this theme is 20 out of 1974: ')
	Corpus_text_amount += Internet
	ThemesQuantitymanual['Интернет']= Internet
	Pravo = input('Please enter amount of text with theme Pravo; total amount of texts with this theme is 10 out of 1974: ')
	Corpus_text_amount += Pravo
	ThemesQuantitymanual['Преступность и право']= Pravo
	print 'Total lilcorpus amount is:', Corpus_text_amount
	for k, v in ThemesQuantitymanual.iteritems():
		print 'There are', v,' texts with theme ',k,' thats', round(percentage(v,Corpus_text_amount), 1), 'percent of corpus'
	return ThemesQuantitymanual
def splitcorpus(corpus,textfrequency, output):
	#littlecorpus = codecs.open('lilcorpus.xml','a')
	filenamecor = output
	print 'starting parsing'
	root = ET.parse(corpus)
	print 'shuffling'
	shuffledtexts = root.findall('./text')
	random.shuffle(shuffledtexts)
	for atype in shuffledtexts: # trying to work with each text
		print 'working' 
		for btype in atype.findall("./tags/tag"): #first we check if tag we associate with theme is present, for that we check all tags of the text
			x = btype.text.encode('utf-8') #just encoding
			print 'still working...'
			for k, v in textfrequency.iteritems():
				print '...'
				if re.search(k, x): #if we find our theme in tags then we add a whole text to new xml doc
					if v == 0:
						print 'OOOOOPA'
						break
					else:
						textfrequency[k] = v-1
						print v
						with codecs.open('corpus'+str(filenamecor)+'.xml','a') as f:
							f.write(ET.tostring(atype, encoding = 'UTF-8'))
			#for k, v in textfrequency.iteritems():
			#	print 'This is amount of texts vs what should have been'
			#	print v
def percentage(part, whole):
  return 100 * float(part)/float(whole)
def comparecorpora(freqdictionary1, freqdictionary2):
	allworddifferences = []
	allmaximalareas = []
	listofmatchedwords = []
	lackingwords = 0
	for k, v in freqdictionary1.iteritems():
		for k2, v2 in freqdictionary2.iteritems():
			if k == k2:
				worddifference = math.fabs(v-v2)
				allworddifferences.append(worddifference)
				listofmatchedwords.append(k)
				if v > v2:
					allmaximalareas.append(v)
				else:
					allmaximalareas.append(v2)
			else: 
				lackingwords +=1
	DifferenceCoefficient = sum(allworddifferences)/ float(sum(allmaximalareas))
	print lackingwords
	print DifferenceCoefficient 
	print 'OF Test!'

#countthemes('annot.opcorpora.no_ambig.xml')
#bibaa = defthemescorpus()
#Texttogramfreq(massive)
#Texttolemmafreq(massive)
#Sampling
# thisis = defthemescorpus()
# splitcorpus('corpusTotalcorpus.xml',thisis, 'UnbSample3')
#TESTING COMPARISON
string1 = ifdocxmlGRAM('corpusGoldSample3.xml')
print 'First step done'
print time.time()
string2 = ifdocxmlGRAM('corpusAvgSample1.xml')
print 'Second step done'
print time.time()
freqdictionary1 = lex_count(string1)
print 'Another step done'
print time.time()
freqdictionary2 = lex_count(string2)
print 'Another step done'
print time.time()
comparecorpora(freqdictionary1, freqdictionary2)
print 'First Testing gold vs avg 1 Complete!'
string3 = ifdocxmlGRAM('corpusAvgSample2.xml')
freqdictionary3 = lex_count(string3)
comparecorpora(freqdictionary1, freqdictionary3)
print 'Testing gold vs avg 2 Complete!'
string4 = ifdocxmlGRAM('corpusAvgSample3.xml')
freqdictionary4 = lex_count(string4)
comparecorpora(freqdictionary1, freqdictionary4)
print 'Testing gold vs avg 3 Complete!'
string5 = ifdocxmlGRAM('corpusUnbSample1.xml')
freqdictionary5 = lex_count(string5)
comparecorpora(freqdictionary1, freqdictionary5)
print 'Testing gold vs unb 1 Complete!'
string6 = ifdocxmlGRAM('corpusUnbSample2.xml')
freqdictionary6 = lex_count(string6)
comparecorpora(freqdictionary1, freqdictionary6)
print 'Testing gold vs unb 2 Complete!'
string7 = ifdocxmlGRAM('corpusUnbSample3.xml')
freqdictionary7 = lex_count(string7)
comparecorpora(freqdictionary1, freqdictionary7)
print 'Testing gold vs unb 3 Complete!'
print 'finished'
