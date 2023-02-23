import os
import re
import sys
import string
import datetime
import pprint
import pandas as pd
import numpy as np
import nltk
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from tqdm.auto import tqdm
from collections import defaultdict, Counter
import matplotlib.pyplot as plt

def freqPlotter(year, yearsHash):
  #plt.figure(figsize=(20, 8))
  for year in yearsHash.keys():
    fdist = FreqDist(yearsHash[year]['keptWords'])
    fdist.plot(20)  
    plt.title(year)

def lexPlotter(lex_scores_list):
  figure, plt = plt.subplot(1,1)
  '''
  multi-bar graph with list of tuples
  x = year
  y = lexical score
  '''

def lexical_diversity(text):
  ''' 
  lexical_diversity captures the frequency of
  new words used for each body of text
  '''
  word_count = len(text)
  vocab_size = len(set(text))
  diversity_score = vocab_size / word_count
  return diversity_score

def wordFreq(yearsHash):
  lex_scores_list = []
  for year in sorted(yearsHash.keys()):
    text = yearsHash[year]['keptWords']
    lex_scores_list.append([year, lexical_diversity(text)])
    '''
    counts = Counter(text)
    words = counts.keys()
    word_freq = counts.values()
    word_freq, words = (list(t) for t in zip(*sorted(zip(word_freq, words)))) # ordered most freq -> less freq
    total_words = sum(word_freq)
    word_freq = [x/total_words for x in word_freq]
    words = words[::-1]
    word_freq = word_freq[::-1]
    freqPlotter(year, yearHash)
    lexPlotter(lex_scores_list)
    '''
  pp = pprint.PrettyPrinter(indent=4)
  pp.pprint(lex_scores_list)
        
def yearExaminer(searchesHash):
  '''
  yearExaminer buckets the results for each searchTerm 
  by year of publication and analyzes the lexicon used
  in the abstracts.
  
  pre-processing: 
      1) lower-case for all words
      2) tokenize to split words from punctuation
      3) separates all stop words to yearsHash[year]['wordsLeft']
      4) separates all punctuation to yearsHash[year]['punctuation']
      5) separates words that contain numbers to yearsHash[year]['numberWords']
      6) lemmitize all remaining words
            - A lemma (plural lemmas or lemmata) is the canonical form, 
              dictionary form, or citation form of a set of words.
  
  analysis:
      1) most frequent 20 words year-over-year
      2) lexical diversity year-over-year
  '''
  stopWords = nltk.corpus.stopwords.words('english')
  punctuation = string.punctuation
  yearsHash = defaultdict(lambda: defaultdict(list))
  lemmatizer = WordNetLemmatizer()
  for query in searchesHash.keys():
    for article in searchesHash[query].keys():
      # word_tokenize splits off punctuation other than periods
      abstract = nltk.tokenize.word_tokenize(searchesHash[query][article]['abstract'].lower()) #1 and #2
      year = searchesHash[query][article]['publication_date'][:4]
      for word in abstract:
        if word in punctuation:
          yearsHash[year]['punctuation'].append(word) #3
        elif word in stopWords:
          yearsHash[year]['stopWords'].append(word) #4
        elif any(map(str.isdigit, word)):
          yearsHash[year]['numberWords'].append(word) #5
        else:
          word = lemmatizer.lemmatize(word) #6
          yearsHash[year]['keptWords'].append(word)
        '''
        # yearsHash[year]['query'] = query #DO OR DO NOT DO BY QUERY? 
        '''
  wordFreq(yearsHash)
  lexical_diversity(yearsHash)
  return(yearsHash)
            