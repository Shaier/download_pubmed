# libraries
from datasets import load_dataset
import os
import json 

# load all of pubmed -- note that this dataset is 360GB+, so I'm loading this in "streaming mode" -- https://huggingface.co/docs/datasets/stream
# https://huggingface.co/datasets/pubmed
full_pubmed = load_dataset('pubmed', streaming=True)

# make directory if it doesn't exist
if not os.path.isdir('pubmed_portions'):
    os.mkdir('pubmed_portions')

# download pubmed in portions
portion_size = 1000000 # 1 mil entries per portion
pubmed_portion = []
counter = 0

# note that I'm only taking the pmid, year, abstract text, abstract title, and authors. There is some more information that you can see by either visiting (https://huggingface.co/datasets/pubmed) or printing one of the entries in the dataset
for idx, entry in enumerate(full_pubmed['train']): 
    try:
        # print(entry)
        pmid = entry['MedlineCitation']['PMID']
        year = entry['MedlineCitation']['DateCompleted']['Year']
        abstract_text = entry['MedlineCitation']['Article']['Abstract']['AbstractText']
        abstract_title = entry['MedlineCitation']['Article']['ArticleTitle']
        abstract_authors_list = entry['MedlineCitation']['Article']['AuthorList']['Author']['LastName']

        if len(abstract_text) > 20 and len(abstract_title) > 5 and len(abstract_authors_list) > 0: # check that the abstract text, title, or authors are not empty
            pubmed_portion.append({'pmid':pmid, 'year':year, 'abstract_text':abstract_text, 'abstract_title':abstract_title, 'abstract_authors_list':abstract_authors_list})

        if idx % 10000 == 0:
            print('idx', idx)

        if idx % portion_size == 0 and len(pubmed_portion)>0:
            # save the pubmed portion
            with open(f'pubmed_portions/pubmed_portion_{counter}.json', 'w') as fp:
                json.dump(pubmed_portion, fp)        
            # reset the list
            pubmed_portion = []
            counter += 1
    except: # any issue with the article
        pass
