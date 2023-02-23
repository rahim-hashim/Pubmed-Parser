import string
from collections import defaultdict
# For download info / documentation on Natural Language Toolkit (nltk):
#    https://www.nltk.org/
import nltk
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw')

def CountFrequency(my_list): 
   '''
   Creating an empty dictionary and count 
   the number of times each term occurs
   '''
   count = {}
   for i in my_list:
    count[i] = count.get(i, 0) + 1
   return count

def lemming_count(searchesHash, top_n_words):
  stopWords = nltk.corpus.stopwords.words('english')
  punctuation = string.punctuation
  lemmatizer = WordNetLemmatizer()
  for query in searchesHash.keys():
    authorHash = defaultdict(list)
    for article in searchesHash[query].keys():
      # word_tokenize splits off punctuation other than periods
      abstract = nltk.tokenize.word_tokenize(searchesHash[query][article]['abstract'].lower()) #1 and #2
      year = searchesHash[query][article]['publication_date'][:4]
      for word in abstract:
        if word in punctuation:
          pass
        elif word in stopWords:
          pass
        elif any(map(str.isdigit, word)):
          pass
        elif '/' in word:
          pass
        elif len(word) < 3:
          pass
        else:
          word = lemmatizer.lemmatize(word)
          authorHash[query].append(word)
    dict_frequency = CountFrequency(authorHash[query])
    dict_ordered = {k: v for k, v in sorted(dict_frequency.items(), key=lambda item: item[1], reverse=True)}
    print(query, list(dict_ordered.keys())[:top_n_words])