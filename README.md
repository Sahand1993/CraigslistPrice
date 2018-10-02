# Price Recommendation Engine
A search engine for getting price statistics of motorcycles sold on Blocket


HOW TO USE:

1. Install pillow and elasticsearch modules for python.
`pip install pillow`
`pip install elasticsearch`

2. Download and run Elasticsearch according to these instructions: https://www.elastic.co/downloads/elasticsearch 

3. Install the elasticsearch python module: ``

3. Start the program with :
`python3 SearchGUI.py`

4. What you can filter on in the fields:
- Query: Specify the search in free text (you can for example write brand, model, color, condition - whatever you want)
- City: Enter a location/city that you want to filter the search on. THIS FIELD IS NOT RECOMMENDED TO USE SINCE SOME CITIES ARE DIVIDED INTO SMALLER REGIONS AND THE MAIN CITY DOES NOT GIVE ANY HITS.
- Type: Select a specific motorcycle type or search amongst all types ("All")
- Maximum Model Year: Select how new motorcycles you want to include in the search result
- Minimum Model Year: Select how old motorcycles you want to include in the search result
