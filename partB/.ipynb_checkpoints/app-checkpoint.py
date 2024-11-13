import logging, sys
logging.disable(sys.maxsize)

import lucene
import os
import json
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query, BooleanQuery, BooleanClause
from org.apache.lucene.search.similarities import BM25Similarity
from flask import request, Flask, render_template

app = Flask(__name__)

# json_file = 'hopper1.json'
#f = open('../spiders/data_scraped.json')
#sample_doc = json.load(f)

def create_index(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    store = SimpleFSDirectory(Paths.get(dir))
    analyzer = StandardAnalyzer()
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

    # BM25 similarity - set ranking
    config.setSimilarity(BM25Similarity())
    
    writer = IndexWriter(store, config)

    metaType = FieldType()
    metaType.setStored(True)
    metaType.setTokenized(False)

    contextType = FieldType()
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    for sample in sample_doc:
        title = sample.get('title')
        content = sample.get('content')
        categories = sample['categories']
        url = sample['link']

        doc = Document()
        doc.add(Field('Title', str(title), metaType))
        doc.add(Field('Text', str(content), contextType))
        doc.add(Field('Tags', str(categories), contextType))
        doc.add(Field('URL', str(url), contextType))
        writer.addDocument(doc)

    writer.close()

def retrieve(storedir, query):
    searchDir = NIOFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))

    # title match receives double rank boost
    parser_title = QueryParser('Title', StandardAnalyzer())
    query_title = BoostQuery(parser_title.parse(query), 2.0)

    # regular text match receives no additional rank boost
    parser_text = QueryParser('Text', StandardAnalyzer())
    query_text = BoostQuery(parser_text.parse(query), 1.0)

    # tag match receives 1.5x rank boost
    parser_tags = QueryParser('Tags', StandardAnalyzer())
    query_tags = BoostQuery(parser_tags.parse(query), 1.5)

    # combine queries using BooleanQuery
    combined_query = BooleanQuery.Builder()
    combined_query.add(query_title, BooleanClause.Occur.SHOULD)
    combined_query.add(query_text, BooleanClause.Occur.SHOULD)
    combined_query.add(query_tags, BooleanClause.Occur.SHOULD)

    # perform search operation
    topDocs = searcher.search(combined_query.build(), 10).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "title": doc.get("Title"),
            "url": doc.get("URL")
            #"text": doc.get("Context")
        })

    return topkdocs

@app.route('/')
def index():
    return render_template('index.html', all_results=[])

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search query
    search_results = []  # store the search res of the query
    print(query)
    if query:  # if there is a query
        lucene.getVMEnv().attachCurrentThread()
        search_results = retrieve('sample_lucene_index', query)
    return render_template('index.html', search_results=search_results)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

if __name__ == '__main__':
    #with open('../spiders/data_scraped.json', 'r') as f:
        #sample_doc = json.load(f)
    #create_index('../sample_lucene_index', sample_doc)
    app.run(host="0.0.0.0", port=80, debug=True)

