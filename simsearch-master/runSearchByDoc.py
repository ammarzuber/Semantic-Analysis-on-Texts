# -*- coding: utf-8 -*-
"""
This script demonstrates finding documents in the corpus which are similar
to a specific document in the corpus. 

Find documents similar to 'document' number 73, which is mhc1.txt lines 
1617 - 1647. This is commentary on the seventh day of creation, when God 
rested. The top match is commentary on the fourth commandment--to obey the 
sabbath (Exodus Chapter 20).

@author: Chris McCormick
"""

from simsearch import SimSearch

# Load the pre-built corpus.S
print('Loading the saved SimSearch and corpus...')
(ksearch, ssearch) = SimSearch.load(save_dir='./text_corpus/')

print('Searching for docs similar to document number 20...')
print('')

# Display the source document.
print('Input - (Doc 8):')
ksearch.printDocSourcePretty(doc_id=10, max_lines=10)

print('')


# Perform the search
results = ssearch.findSimilarToDoc(doc_id=10, topn=1)

# Print the top results
ssearch.printResultsBySourceText(results, max_lines=8)

# Retrieve the tf-idf vectors for the input document and it's closest match.
vec1_tfidf = ksearch.getTfidfForDoc(10)
vec2_tfidf = ksearch.getTfidfForDoc(results[0][0])

print('')    

# Interpret the top match.
ssearch.interpretMatch(vec1_tfidf, vec2_tfidf)