import re
import string
from tqdm.notebook import tqdm
from collections import defaultdict
import urllib.request, urllib.parse, urllib.error
# For download info / documentation on BeautifulSoup:
#    https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup

def linksParser(termLinks, searchParameters, searchTerm):
	'''
	linksParser reads each URL from PMID_ListGenerator output 
	and parses specified info
	'''
	print('  '+ searchTerm)
	articleCount = 0; abstract_text = []
	searchesHash = defaultdict(lambda: defaultdict(list)) # primary key = PMID
	for link in tqdm(termLinks):
		searchHash = defaultdict(str)
		authorAffiliationDict = defaultdict(list)
		affiliationDict = defaultdict(str)
		searchHash['articleCount'] = articleCount
		articleCount += 1
		# Open, read and process link through BeautifulSoup
		r1 = urllib.request.urlopen(link).read()
		soup = BeautifulSoup(r1, "html.parser")
		# ARTICLE NAME Parser
		article_title = soup.find('title').text
		searchHash['article_title'] = article_title
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
					if len(tag.attrs['content'].split('/')) == 2: # date format (YYYY/MM)
						tag.attrs['content'] = tag.attrs['content'].split('/')[0]
					searchHash['publication_date'] = tag.attrs['content']
				elif tag.attrs['name'] == 'citation_author':
					author_list.append(tag.attrs['content'])
				elif tag.attrs['name'] == 'citation_author_institution':
					author_institutions.append(tag.attrs['content'])
				elif tag.attrs['name'] == 'citation_pmid':
					PMID = tag.attrs['content']
				elif tag.attrs['name'] == 'citation_doi':
					searchHash['doi'] = 'doi.org/' + tag.attrs['content']
		searchHash['authors'] = author_list
		searchHash['author_institutions'] = author_institutions
		searchesHash[PMID] = searchHash
		# AUTHOR AFFILIATION Parser
		# author_soup = soup.find_all("span", {"class": "authors-list-item"})
		# for index, author_info in enumerate(author_soup):
		# 	author = author_list[index]
		# 	author_text = author_info.text.split()
		# 	author_affiliations = [item for item in author_text if item.isnumeric()]
		# 	affiliations = author_info.find_all(class_='affiliation-link')
		# 	affiliation_list = [affiliation_title['title'] for affiliation_title in affiliations]
		# 	for affiliation_index, affiliation_number in enumerate(author_affiliations):
		# 		affiliationDict[affiliation_number] = affiliation_list[affiliation_index]
		# 		authorAffiliationDict[author].append(affiliation_number)
		# searchHash['affiliation_dict'] = affiliationDict
		# searchHash['author_affiliation_dict'] = authorAffiliationDict
		# # PAPER LINK Parser
		# paper_soup = soup.find_all("a", {"class": "link-item"})
		# for paper in paper_soup:
		# 	print(paper['href'])
		# 	break
	return searchesHash