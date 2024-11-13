# Overview of System
 ## Architecture
From part A, we collected data from our web crawler (modified to get 800MB) into a
 .json file. The scraped data is indexed with PyLucene, which helps handle the different
 text fields such as title, content, tags, and URL. With this indexed data, a search query
 can be inputted and processed with PyLucene’s query parser. Users can access the web
 interface to input search queries and review the results. Using the implemented ranking
 with the BM25 model, stop words handling, and custom rank boosting, the most relevant
 documents are retrieved and the top ten search results appear.
Seed URL: Louisiana Highway
 Scraped: 70,000 web pages
 Total of 790MB
 ## Index Structures
We used several text fields for our indexing. We scraped titles, text, tags, and URLs from
 the Wikipedia webpages and stored them in the JSON. For the analyzer, we chose the
 StandardAnalyzer because it is the most general analyzer which meets our needs, as
 Wikipedia pages are mostly textual content, so the StandardAnalyzer works well in this
 case to tokenize and process the text.
 ## Search Algorithm
The queries are processed through searching the title, body, and category fields of the
 documents. Alongside the BM25 similarity model, the BoostQuery function is applied to
 the three different types of fields to give higher overall relevance scores. For titles, there
 is a double boost in ranking. Regular body text receives no additional boost. Lastly,
 categories get a 1.5x boost. After boosting the queries, we used PyLucene’s main search
 algorithm which uses the BooleanQuery mechanism. The parser takes the user input and
 then PyLucene combines the queries and singles out the titles, text, and tags with boolean
 logic.
## Limitations of System
The system does not use a custom snippet-generation algorithm to display a snippet for each
 search result, it only shows the title for the search result.
 Our system only scrapes about 800 MB of data from Wikipedia. While this may seem like a lot,
 this is still a relatively small amount of data compared to all of which Wikipedia can actually provide.
 This can result in limited answers and it may not have the extent of information that a user is searching
 for. Additionally, loading the results of a query takes some time. If we were to build upon this project, we
 could parallelize the scraping and indexing process in order to account for this limitation.
 ## Instructions on How to Deploy the System
 To deploy the website:
 Flask must be installed on the system that we run the website on. The site can be deployed by the
 commands in the group32/group32/partB/ directory:
 export FLASK_APP=app
 Flask run-h 0.0.0.0-p 8080
 This will open the website using port 8080.
 Indexing/query ranking algorithm:
 The algorithm can be tested by running the command “python tamper_lucene.py”. This takes the
 data from data_scraped.json in the spiders folder and ranks the documents. The top 10 ranking documents
 are then output into the terminal with their scores, the title, and the URL. Currently, we have four queries
 hard coded into the program that have their ranked documents output to the terminal when you run
 tamper_lucene.py.
 Index Time: The total time it takes to index the data is ~45 seconds to 1 minute. The query ranking itself
 should be instantaneous.
 ## Web Framework
 A web-application (e.g. Web Archive) that can be deployed to a webserver like Tomcat.
 Wecreated our website using flask. In index.html, we include code for the structure of our site. At
 the top of the page is the title of our search engine. By clicking on the title, you can return to the
 homepage (at “/”). When a query is entered into the search bar and the button is clicked, the ranking
 algorithm (created with Pylucene) is run on the entered query terms. The output is written to a .json file.
 Results are rendered to the user based on the data in the .json file. If the file is empty, nothing is
 displayed. Additionally, the page re-routes to “search?query=[QUERY]”. Our style.css file includes
 formatting for the website.
 
<img width="571" alt="query_results_terminal" src="https://github.com/user-attachments/assets/f86fed2b-f456-434b-9858-a529018793ea">
<img width="545" alt="pie_search_query" src="https://github.com/user-attachments/assets/40a518eb-ba24-4163-8094-33f1fb606764">
<img width="555" alt="link_and_deployment" src="https://github.com/user-attachments/assets/f5a39af4-ece9-46ea-ab9a-2bfe83b1218c">
