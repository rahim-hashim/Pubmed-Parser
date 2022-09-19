![Selected dataset (though others are compatible as well for this code](docs/images/SemanticScholar_Header.png)

# Pubmed + Semantic Scholar

### Python-Based Scraper and Textual Analysis

[The NSF released data in 2019](https://ncses.nsf.gov/pubs/nsb20206/data) stating that 2,555,959 scientific articles were published in 2018, or rather, \~4.86 publications per minute. And as principle investigators expand their research programs across disciplines, and buzzwords make their way into more and more studies (see Pubmed query: 'Artificial Intelligence', 'Reinforcement Learning'), it has become exceedingly more difficult to keep up to date with the immense volume of research being published. In order for researchers to tackle the publication volume bottleneck, we must create stricter initial filters specifying research highly relevant to our interests. 

Here, we have built a modular Python-based package to scrape the publicly-available database [Pubmed](https://pubmed.ncbi.nlm.nih.gov/), with help from Allen Institute's [Semantic Scholar](https://www.semanticscholar.org/me/research) API, which will allow us to analyze the language and structure around abstracts for peer-reviewed scientific articles. An advantage of this toolkit is that it allows for maximum search flexibility, using the same advanced query constructions as the NCBI database advanced search itself, allowing for cross-author and cross-domain investigations. The goal is to provide a way for scientific researchers to investigate scientific literature with greater precision, by 1) narrowing the initial filter of papers that make it to your To-Do list and 2) generating digestible overview pages for subfields and authors. 

To start, clone this repository, and test out different searches on the Pubmed main page to get a sense for the types of queries you might be interested in.

Click on advanced, and check out the [User Guide](https://pubmed.ncbi.nlm.nih.gov/help/) to build specific query constructions, which will be very helpful for using this tool. Next, open the [pubmed-parser.ipynb](pubmed-parser.ipynb) notebook. All the following steps should be available in the notebook itself.
