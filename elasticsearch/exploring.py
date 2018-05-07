#Trying out the elastic search python interface

import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch()

f_in = open("../dataset/motorcycles_python.json", "r")

actions = (json.loads(line) for line in f_in)

bulk(es, actions)