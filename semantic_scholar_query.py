import os
import json
import numpy as np
import urllib.request
from textwrap import indent
from pprint import pprint, pformat

def semantic_scholar_query(PMID):
	"""
	Queries the Semantic Scholar API for the given PMID and returns the
	citation count and the weighted citation count

	Args:
		PMID (str): A PubMed ID

	Returns:
		citation_count (int): The number of citations for the given PMID
		ss_citation_count (int): The weighted number of citations for the given PMID
	"""
	fields = ['title',
						'journal',
						'year',
						'fieldsOfStudy',
						'referenceCount',
						'citationCount',
						'influentialCitationCount',
						'influentialCitationCount',
						'authors.name,authors.hIndex']
	fields_str = ','.join(fields)
	semantic_scholar_base = 'https://api.semanticscholar.org/graph/v1/paper/PMID:<>?fields=' + fields_str
	semantic_scholar_url = semantic_scholar_base.replace('<>', PMID)
	r = urllib.request.urlopen(semantic_scholar_url).read().decode('utf-8')
	ss_dict = json.loads(r)
	citation_count = ss_dict['citationCount']
	ss_weighted_citation_count = ss_dict['influentialCitationCount']
	return citation_count, ss_weighted_citation_count

def semantic_scholar_search(searchesHash, verbose=False):
	"""
	semantic_scholar_search searches the Semantic Scholar API for the given
	PMID and returns the citation count and the weighted citation count

	Args:
		searchesHash (dict): A dictionary of PubMed IDs (PMIDs) and their
			associated search terms
		verbose (bool): If True, print all the search terms and the results of
			the Semantic Scholar API query

	Returns:
		searchesHash (dict): The input dictionary with the citation count and
			the weighted citation count added to each PMID
	"""
	for q_index, query in enumerate(searchesHash):
		print('Query: {}'.format(query))
		for r_index, PMID in enumerate(searchesHash[query]):
			try:
				citation_count, ss_citation_count = semantic_scholar_query(PMID)
			# maximum requests hit for Semantic Scholar (100 per 5 minutes)			
			except:
				citation_count = np.nan
				ss_citation_count = np.nan
			searchesHash[query][PMID]['citation_count'] = citation_count
			searchesHash[query][PMID]['semantic_scholar_citation_count'] = ss_citation_count
			if (q_index < 5 and r_index < 5) or verbose == True:
				print_str = 'Title: {} ({})'.format(
									searchesHash[query][PMID]['article_title'],
									searchesHash[query][PMID]['publication_date'])
				print(indent(pformat(print_str), 
										prefix='  '))
				print(indent(pformat('PMID: {}'.format(PMID)),
										prefix='\t'))
				print(indent(pformat('Citation Count: {}'.format(citation_count)),
										prefix='\t'))
				print(indent(pformat('Semantic Scholar Citation Count: {}'.format(ss_citation_count)),
										prefix='\t'))
	return searchesHash