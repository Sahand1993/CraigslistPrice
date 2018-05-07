#Testing to search
from elasticsearch import Elasticsearch

es = Elasticsearch()
es.indices.refresh(index="simple")
#search (query has to be modified later...)
res = es.search(index="simple", body={"query": {"match_all": {}}})

#print result
print("Got " + str(res['hits']['total']) + " hits")
for hit in res['hits']['hits']:
    print(hit);
    print();
    print("ID: " + str(hit["_source"]["id"]))
    print("TITLE: " + str(hit["_source"]["title"]))
    print("DATE: " + str(hit["_source"]["date"]))
    print("LOCATION: " + str(hit["_source"]["location"]))
    print("PRICE: " + str(hit["_source"]["price"]))
    print("SELLER: " + str(hit["_source"]["sellerName"]))
    print("DESCRIPTION: " + str(hit["_source"]["description"]))
    print("MODEL YEAR: " + str(hit["_source"]["modelYear"]))
    print("VEHICLE TYPE: " + str(hit["_source"]["vehicleType"]))
    print("URL: " + str(hit["_source"]["url"]))
    #Only print first hit
    break
