import re
import string
from tqdm import tqdm
import urllib.request, urllib.parse, urllib.error
# For download info / documentation on BeautifulSoup:
#    https://www.crummy.com/software/BeautifulSoup/bs4/doc/
from bs4 import BeautifulSoup
# For download info / documentation on unidecode:
#    https://pypi.python.org/pypi/Unidecode#downloads
from unidecode import unidecode
from searchObjects import Author, Affiliation
from Regions import countryList, stateDict, alphaSpace

def linksParser(termCounter, termLinks, searchParameters, searchTerm, searchesHash):
    '''linksParser reads each URL from PMID_ListGenerator output and parses specified info'''
    print('  '+ searchTerm)
    articleCount = 0; abstract_text = []
    for link in tqdm(termLinks):
        searchHash = {}
        searchHash['articleCount'] = articleCount
        articleCount += 1
        # Open, read and process link through BeautifulSoup
        r1 = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(r1, "html.parser")
        # PMID Parser
        link_split = link.split('/')
        PMID = link_split[-1]
        # ARTICLE NAME Parser
        articleTitleSearch = soup.find_all('h1')
        articleTitle_uncleaned = str(articleTitleSearch[1])
        articleTitle_cleaned = articleTitle_uncleaned[4:-5]
        articleTitle = unidecode(articleTitle_cleaned.strip('\n'))
        searchHash['articleTitle'] = articleTitle
        # META INFO (journal title, date published)
        metaSearch = soup.find_all(attrs={'name':'description'})
        metaInfo_uncleaned = metaSearch[1]['content'].split('.')
        # JOURNAL NAME Parser
        journalTitle = metaInfo_uncleaned[0]
        if journalTitle[:6] == 'PubMed': #Some articles have journal/date published in distinct locations, in which case search captures "PubMed comprises more..."
            journalSearch = soup.find_all("h3", attrs={'class' : 'label'})
            for result in journalSearch:
                if 'Source' in result:
                    journalResult_uncleaned = str(result.next_sibling)
                    journalResult_uncleaned1 = journalResult_uncleaned.replace('\n', '')
                    journalResult_cleaned = re.findall('">(.*?)<br/>', journalResult_uncleaned1)
                    journalResult_cleaned1 = journalResult_cleaned[0].split(';')
                    journalTitle = journalResult_cleaned1[0]
                    datePublished = journalResult_cleaned1[1].strip('.')
        searchHash['journalTitle'] = metaInfo_uncleaned[0].strip()
        # DATE PUBLISHED Parser
        datePublished_uncleaned = metaInfo_uncleaned[1].split(';')
        datePublished = datePublished_uncleaned[0]
        if len(datePublished) < 6:
            for item in metaInfo_uncleaned:
                if 'Epub' in item:
                    datePublished_uncleaned1 = item.split('Epub ')
                    datePublished = datePublished_uncleaned1[1]
        searchHash['datePublished'] = datePublished.lstrip()
        # ABSTRACT Parser
        abstractSearch = soup.find('div', class_ = 'abstr')
        abstract_uncleaned = re.findall('p>(.*?)</p', str(abstractSearch))
        if len(abstract_uncleaned) > 0:
            re.sub("[\(\[]<.*?>[\)\]]", "", str(abstract_uncleaned))
            abstract = str(abstract_uncleaned[0])
        else:
            abstract = ''
        searchHash['abstract'] = abstract
        # AUTHOR INFO Parser
        authorList = []; supsList = []
        authorSearch = str(soup.find('div', class_ = 'auths'))
        authors_newsplit = re.findall('<a href(.*?)>', authorSearch)
        sup_newsplit = authorSearch.split('<a href')
        if not authors_newsplit:
            author = Author()
            authorList.append(author)
            supsList.append({})
        else:
            for author_index, authorSplit in enumerate(authors_newsplit):
                authors_uncleaned = authorSearch.split(authorSplit)
                authors_uncleaned1 = authors_uncleaned[1].split('/a')
                author = Author()
                author.name = authors_uncleaned1[0][1:-1]
                author.listed_order = author_index
                sups_dict = {}
                try:
                    sup_uncleaned = re.findall('<sup>(.*?)</sup>', str(sup_newsplit[author_index+1]))
                    for sup in sup_uncleaned:
                        sup = sup.strip(',')
                        sups_dict[sup] = {}
                except:
                    pass
                authorList.append(author)
                supsList.append(sups_dict)
            authorInfoSearch = soup.find("div", class_ = 'afflist')
            authorInfo_uncleaned = re.findall('<dt>(.*?)</dd>', str(authorInfoSearch))
            if len(authorInfo_uncleaned) > 0:
                for info in authorInfo_uncleaned:
                    affiliation = Affiliation()
                    authorInfo_uncleaned1 = info.split('</dt><dd>')
                    # AUTHOR INFO Parser
                    sup = authorInfo_uncleaned1[0]
                    authorInfo = authorInfo_uncleaned1[1].replace('\t', ' ')
                    # In some cases, sup is kept in authorInfo (e.g. 'a Department of Epidemiology')
                    if authorInfo[:2] in alphaSpace:
                        authorInfo = authorInfo[2:]
                    authorInfo = authorInfo.split(',')
                    for affiliate_info in authorInfo:
                        #print(affiliate_info)
                        if 'Department' in affiliate_info:
                            affiliation.department = affiliate_info.strip()
                        elif 'University' in affiliate_info:
                            affiliation.university = affiliate_info.strip()
                        elif 'Institute' in affiliate_info:
                            affiliation.institute = affiliate_info.strip()
                        elif affiliate_info in countryList:
                            affiliation.country = country.strip()
                        else:
                            affiliate_info_split = affiliate_info.split()
                            for word in affiliate_info_split:
                                if '@' in word:
                                    affiliation.email = word
                                elif word in stateDict:
                                    affiliation.state = word
                                    affiliation.country = 'US'
                                elif len(word) >= 5:
                                    if word[:5].isdigit():
                                        affiliation.zipcode = word[:5]
                    for a_index, author in enumerate(authorList):
                        if sup in supsList[a_index].keys():
                            supsList[a_index][sup] = affiliation
            for a_index, author in enumerate(authorList):
                authorList[a_index].affiliations = supsList[a_index] 
            searchHash['authors'] = authorList
        searchesHash[PMID] = searchHash
    return searchesHash