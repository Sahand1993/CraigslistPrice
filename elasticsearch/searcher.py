import json
from statistics import mean, median

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

PATH_TO_DATASET = "../dataset/mini.json"
CUTOFF = 0.8    # Results with score less than 0.8 * max_score will not
                # contribute to price estimate
INDEX_NAME = "simple"
TITLE_WEIGHT = 0.5
DESCRIPTION_WEIGHT = 1 - TITLE_WEIGHT
# maximum number of similar objects returned by Searcher.similar()
MAX_OBJECTS = 19000


# TODO: look at Stemming, stop words and weighting between
# title and description

class Searcher(object):
    def __init__(self):
        self.es = Elasticsearch()

        if self.es.indices.exists(INDEX_NAME):
            print('Deleting index "{}"'.format(INDEX_NAME))
            self.es.indices.delete(INDEX_NAME)

        self.create_index(PATH_TO_DATASET)

        # title_weight is how many more times important title_weight
        # is compared to description weight
        self.title_weight = TITLE_WEIGHT / DESCRIPTION_WEIGHT

    def construct_query_body(self, q = "", **kwargs):
        query = {
"query": {
    "bool": {}
}  
        }

        if q:
            query["query"]["bool"]["must"] = {
            "multi_match": {
                "type": "cross_fields",
                "query": q,
                "fields": ["title^"+str(self.title_weight), "description"], # Weighting title field
                "operator": "or" # Or is probably the default value
            }
            }

        query_filters = []
        if "min_model_year" in kwargs:
            query_filters.append(\
            {
                "range":{
                    "modelYear": {
                        "gte": kwargs["min_model_year"]
                    }
                }
            }
            ) 

        if "max_model_year" in kwargs:
            query_filters.append(\
            {
                "range":{
                    "modelYear": {
                        "lte": kwargs["max_model_year"]
                    }
                }
            }
            ) 
        
        if "location" in kwargs:
            query_filters.append(\
            {
                "term": {
                    "location":kwargs["location"]
                }
            }
            )
        
        if "vehicle_type" in kwargs:
            query_filters.append(\
            {
                "term": {
                    "vehicleType": kwargs["vehicle_type"]
                }
            }
            )
                
        query["query"]["bool"]["filter"] = query_filters

        return query

    def price(self, query = "", **kwargs):
        """
            Calculates median, average, max and min price
            for a query.
            @ query: 
        """
        similar = self.similar(query, **kwargs)
        max_price_obj = max( similar, key = lambda obj: obj["_source"]["price"] ) # object with highest price
        min_price_obj = min( similar, key = lambda obj: obj["_source"]["price"] ) # object with lowest price
        avg = mean(map(lambda obj: obj["_source"]["price"], similar)) # average price
        med = median( map( lambda obj: obj["_source"]["price"], similar ) ) # median price

        result = {
        "median_price" : med,
        "average_price" : avg,
        "max_price" : max_price_obj["_source"]["price"],
        "min_price" : min_price_obj["_source"]["price"],
        "max_price_object" : max_price_obj,
        "min_price_object" : min_price_obj,
        }
        return result

    def search(self, query = "", **kwargs):
        """
        Takes search query parameters and returns results from index 
        """
        query_body = self.construct_query_body(query, **kwargs)
        
        print("Searching with request body: \n{}".format( json.dumps(query_body, indent=4, sort_keys=True) ))

        return self.es.search(index = INDEX_NAME, body = query_body, size = 10, scroll = "2m")
    
    def similar(self, query = "", **kwargs):
        """ 
        Returns all ads that are similar enough to the most similar ad
        using CUTOFF.
        Args:
            query: query string
        kwargs:
            min_model_year: minimum model year
            max_model_year: maximum model year
            location: location
            vehicle_type: vehicle type
        """
        res = self.search(query, **kwargs)

        total = res["hits"]["total"]
        max_score = res["hits"]["max_score"]
        hits = res["hits"]["hits"]
        sid = res["_scroll_id"] # scroll_id. Used to get next "page" of results
        
        similar = [] # all ads which are similar enough to query
        while len(hits) > 0:
            stop = self.similar_in_hits(similar, hits, max_score)

            if stop:
                break

            res = self.es.scroll(scroll_id = sid, scroll = "2m")
            hits = res["hits"]["hits"]
            sid = res["_scroll_id"] # get next scroll_id

        return similar

    def similar_in_hits(self, similar, hits, max_score):
        """
            Takes list of hits and returns list with those that have 
            score/max_score >= CUTOFF
        """
        for ad in hits:
            score = ad["_score"]

            if max_score:
                if score / max_score < CUTOFF:
                    return True

            if len(similar) > MAX_OBJECTS:
                return True

            similar.append(ad)
        return False

    def create_index(self, file_path):
        """
            Takes path to file containing JSON-formatted data
            and indexes into Elasticsearch index.
        """
        print('Creating index "{}"'.format(INDEX_NAME))

        request_body = {
"settings":{
    "index":{
        "number_of_shards":1,
        "number_of_replicas":0
    }
},
"mappings":{
    "motorcycle":{
        "properties":{
            "location": {
                "type":"keyword",
            },
            "vehicleType": {
                "type": "keyword",
            },
            "description":{
                "type":"text",
                "analyzer":"swedish",
            },
        }
    }
}
        }
        self.es.indices.create(index = INDEX_NAME, body = request_body)
        f_in = open(PATH_TO_DATASET, "r")
        actions = (json.loads(line) for line in f_in)
        print("Performed bulk index: {}".format(bulk(self.es, actions)))
        self.es.indices.refresh(index = "simple")

# # Example usage

# searcher = Searcher()
# res = searcher.price("honda", location = "vänersborg", min_model_year=2009, vehicle_type="sport")
# print("""

# Average price: {}
# Median price: {}
# Max price: {}
# Min price: {}
# Most expensive object: {}
# Least expensive object: {}

#     """.format(\
#         res["average_price"],
#         res["median_price"],
#         res["max_price"],
#         res["min_price"],
#         json.dumps(res["max_price_object"], indent = 4),
#         json.dumps(res["min_price_object"], indent = 4)
#         ))