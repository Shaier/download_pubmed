# Download all of PubMed abstracts 
## (plus some other info: pmid, year, abstract text, abstract title, and authors)

## Setup:
### Environment stuff
#### in the terminal: 
```
conda create -n download_pubmed python=3.10
conda activate download_pubmed
conda install -c huggingface -c conda-forge datasets
```
### Data stuff
#### in the terminal: 
```
git clone https://github.com/Shaier/download_pubmed.git
cd download_pubmed/
python pubmed_download.py
```
