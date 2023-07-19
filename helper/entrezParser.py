import re
import datetime
import urllib.request

# eSearchLinkGenerator : Generates URL using user-specified [Database][SearchTerms][NumOfPMIDs] for NCBI Entrez Search Engine
#	Base URL : https://eutils.ncbi.nlm.nih.gov/entrez/eutils/einfo.fcgi
#	For more info on Entrez : https://www.ncbi.nlm.nih.gov/books/NBK25499/#chapter4.ESearch
def eSearchLinkGenerator(url, searchParameters, api=None): 
	print('Generating Entrez XML...')
	urlList = []
	url = url.split('=')
	for term in searchParameters.searchTerms:
		termSplit = term.split (' ')
		finalTerm = ''
		for word in termSplit:
			finalTerm += word + '+'
		databaseTemp = searchParameters.database + url[1]
		finalTerm = finalTerm[:-1] # remove trailing '+' from finalTerm
		finalTerm += url[2]
		articleVolumeTemp = str(searchParameters.searchLimit) + url[3]
		indexTemp = str(searchParameters.startIndex) + url[4]
		updated_url = '='.join([url[0], databaseTemp, finalTerm, articleVolumeTemp, indexTemp])
		if api != None:
			updated_url += '&api_key=' + api
		urlList.append(updated_url)
		print('   [' + term + '] complete')
	return urlList


# PMID_ListGenerator : Reads eSearchLinkGenerator output and generating a list of PMIDs resulting from [SearchTerms] search
def PMID_ListGenerator(eSearchList):
	print('\nGenerating list of PMIDs...')
	finalList = []
	for term in eSearchList:
		r = urllib.request.urlopen(term).read().decode('utf-8')
		PMID_List = re.findall('<Id>(.*?)</Id>', r)
		prefix = 'https://www.ncbi.nlm.nih.gov/pubmed/'
		resultsList = []
		for PMID in PMID_List:
			link = prefix+PMID
			resultsList.append(link)
		finalList.append(resultsList)
		searchTerm = re.findall('<From>(.*?)</From>', r)[0]
		print('  ' + searchTerm + ':', len(PMID_List), 'results')
	return finalList