import re
import string
from tqdm.notebook import tqdm
from collections import defaultdict
import urllib.request, urllib.parse, urllib.error
# For download info / documentation on BeautifulSoup:
#    https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

def linksParser(termCounter, termLinks, searchParameters, searchTerm, searchesHash):
    '''linksParser reads each URL from PMID_ListGenerator output and parses specified info'''
    print('  '+ searchTerm)
    articleCount = 0; abstract_text = []
    for link in tqdm(termLinks):
        searchHash = defaultdict(str)
        searchHash['articleCount'] = articleCount
        articleCount += 1
        # Open, read and process link through BeautifulSoup
        r1 = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(r1, "html.parser")
        # PMID Parser
        #link_split = link.split('/')
        #PMID = link_split[-1]
        # ARTICLE NAME Parser
        articleTitle = soup.find('title').text
        searchHash['articleTitle'] = articleTitle
        # META INFO (journal title, date published)
        meta = soup.find_all('meta')
        author_list = []
        author_institutions = []
        for tag in meta:
          if 'name' in tag.attrs.keys():
            if tag.attrs['name'] == 'citation_journal_title':
              searchHash['journal_title'] = tag.attrs['content']
            elif tag.attrs['name'] == 'citation_journal_abbrev':
              searchHash['journal_title_abv'] = tag.attrs['content']
            elif tag.attrs['name'] == 'citation_publisher':
              searchHash['publisher'] = tag.attrs['content']
            elif tag.attrs['name'] == 'citation_abstract':
              searchHash['abstract'] = tag.attrs['content']
            elif tag.attrs['name'] == 'citation_keywords':
              keywords_uncleaned = tag.attrs['content'].split(';')
              keywords = [keyword.strip().rstrip('.').lower() for keyword in keywords_uncleaned]
              searchHash['keywords'] = keywords
            elif tag.attrs['name'] == 'citation_publication_date' or tag.attrs['name'] == 'citation_online_date':
              searchHash['publication_date'] = tag.attrs['content']
            elif tag.attrs['name'] == 'citation_author':
              author_list.append(tag.attrs['content'])
            elif tag.attrs['name'] == 'citation_author_institution':
              author_institutions.append(tag.attrs['content'])
            elif tag.attrs['name'] == 'citation_pmid':
                PMID = tag.attrs['content']
        searchHash['authors'] = author_list
        searchHash['author_institutions'] = author_institutions
        searchesHash[PMID] = searchHash
    return searchesHash