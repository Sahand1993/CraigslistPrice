# Price Recommendation Engine
A search engine for getting price statistics of motorcycles sold on Blocket


HOW TO USE:

1. Make sure you have "pillow" installed (pip install pillow) in order to use the Python GUI

2. Download and run Elasticsearch according to these instructions: https://www.elastic.co/downloads/elasticsearch 

3. Start the program with :
`python3 elasticsearch/SearchGUI.py`

4. What to enter in the fields:

Query (optional): Specify the search in free text (you can for example write brand, model, color, condition - whatever you want)

City (optional): Enter a location/city that you want to filter the search on

Type: Select a specific motorcycle type or search amongst all types ("All")

Maximum Model Year: Select how new motorcycles you want to include in the search result

Minimum Model Year: Select how old motorcycles you want to include in the search result
