import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import NotFoundError

PATH_TO_DATASET = "../dataset/motorcycles_python.json"
CUTOFF = 0.8 # Results with score less than 0.8 * max_score will not contribute to price estimate
K = 15 # We take top K to provide price recommendation
INDEX_NAME = "blocket"
TITLE_WEIGHT = 0.5
DESCRIPTION_WEIGHT = 1 - TITLE_WEIGHT


## TODO: look at Stemming, stop words and weighting between 
## title and description

class Searcher(object):
	def __init__(self):
		print("hej")
		self.es = Elasticsearch()

		if self.es.indices.exists(INDEX_NAME):
			print('Deleting index "{}"'.format(INDEX_NAME))
			self.es.indices.delete(INDEX_NAME)

		self.create_index(PATH_TO_DATASET)

		# title_weight is how many more times important title_weight
		# is compared to description weight
		self.title_weight = TITLE_WEIGHT/DESCRIPTION_WEIGHT

	def search(self, query, min_model_year = None, max_model_year = None, city = ""):
		"""
			Takes search query and returns price recommendation.
		"""
		
		query = {"query": {
					"bool":{
						"must":{
							"multi_match": {
								"type": "cross_fields", # This means that we 
								"query": query,
								"fields": ["title^"+str(self.title_weight), "description"], # Weighting title field
								"operator": "or" # Or is probably the default value
							}
						},
						"filter":{
							"term":{
								"location":"uppsala"
							}
						},
						"must_not":[
							{"range": {
								"modelYear":{"lte": min_model_year}
							}},
							{"range":{
								"modelYear":{"gt": max_model_year}
							}}
						]
					}
				}
			}
		if min_model_year:
			query["query"]["bool"]["must_not"] = [
											{
												"range":{
													"modelYear": {"lt": min_model_year}
												}
											}
										]

		if max_model_year:
			query["query"]["bool"]["must_not"].append({
					"range":{
						"modelYear": {"gt": max_model_year}
					}
				})
			
		if city:
			query["query"]["bool"]["filter"]["term"] = {"location":city.lower()}

		res = es.search(index = "simple", body = query, size = 1000, scroll = "2m")
		total = res["hits"]["total"]
		max_score = res["hits"]["max_score"]
		hits = res["hits"]["hits"]
		sid = res["_scroll_id"]
		
		similar = None # all ads which are similar enough to query

		# Alternative 1:
		# 1. Do tf-idf ranked search in the title.
		# 2. Do tf-idf ranked search in the body.
		# 3. Do a score union.
		# 4. Pick first k that have the right model 
		# year and take average, median, maximum 
		# and minimum price out of these.
		# 5. If you can't find k motorcycles for 
		# that year, try the nearest years, and 
		# continue from 4. until you have k motorcycles

		# Alternative 2:
		# Put body and description together in one field.
		# Do same as above

		# Alternative 3:
		# train an MLP to take the factors into account and then
		# return a price, based on
		return None

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
								"type":"text",
								"analyzer":"swedish"
							},
							"description":{
								"type":"text",
								"analyzer":"swedish"
							}
						}
					}
				}
			}
		self.es.indices.create(index = INDEX_NAME, body = request_body)
		f_in = open(PATH_TO_DATASET, "r")
		actions = (json.loads(line) for line in f_in)
		bulk(self.es, actions)
		self.es.indices.refresh(index = INDEX_NAME)

searcher = Searcher()
