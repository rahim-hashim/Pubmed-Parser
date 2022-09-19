import pandas as pd

def construct_dataframe(searchesHash: dict) -> pd.DataFrame:
	"""
	construct_dataframe creates a pandas dataframe
	containing all article data for each search term

	Args:
		searchesHash (dict): multi-nested dictionary containing all article data for each search term

	Returns:
		df (pandas dataframe): pandas dataframe containing all article data for each search term
	"""
	print('\nConstructing dataframe...')
	df = pd.DataFrame()
	for query in searchesHash.keys():
		for PMID in searchesHash[query].keys():
			for author in searchesHash[query][PMID]['authors']:
				authorHash = {}
				authorHash['author'] = author
				authorHash['PMID'] = PMID
				authorHash_added = dict(authorHash, **searchesHash[query][PMID])
				collaborators = searchesHash[query][PMID]['authors'][:]
				# Unncessary columns to remove
				remove_columns = ['authors', 'journal_title_abv', 'publisher']
				authorHash_added.pop('authors')
				authorHash_added.pop('journal_title_abv')
				collaborators.remove(author)
				authorHash_added['collaborators'] = collaborators
				df = df.append(authorHash_added, ignore_index=True)
	return df