#Testing to search
from elasticsearch import Elasticsearch

#The user should be able to provide these values as input through the user interface.
#-----------------------
query = "Honda TRX700 vägreggad honda"
city = "Eskilstuna"
vehicle_type = "Sport"
min_price = 17000
max_price = 20000
min_model_year = 2017
max_model_year = 2017
#-----------------------
max_number_of_search_results = 5;
es = Elasticsearch()
es.indices.refresh(index="simple")

if city == "All" and vehicle_type == "All":
    elastic_query = {
        "query":{
                "bool":{
                    "should":[
                        {"match": {"title":  query}},
                        {"match": {"description": query}}],
                    "filter":{
                        "range":{
                            "price":{
                                "gte": min_price,
                                "lte": max_price
                            }
                        },
                        "range":{
                            "modelYear":{
                                "gte": min_model_year,
                                "lte": max_model_year
                            }
                        }
                    }
                }
        },
        "size": max_number_of_search_results
    }

elif vehicle_type == "All":
    elastic_query = {
        "query":{
                "bool":{
                    "must":
                        {"match": {"location": city}},
                    "should":[
                        {"match": {"title":  query}},
                        {"match": {"description": query}}],
                    "filter":{
                        "range":{
                            "price":{
                                "gte": min_price,
                                "lte": max_price
                            }
                        },
                        "range":{
                            "modelYear":{
                                "gte": min_model_year,
                                "lte": max_model_year
                            }
                        }
                    }
                }
        },
        "size": max_number_of_search_results
    }
        
elif city == "All":
    elastic_query = {
        "query":{
                "bool":{
                    "must":
                        {"match": {"vehicleType": vehicle_type}},
                    "should":[
                        {"match": {"title":  query}},
                        {"match": {"description": query}}],
                    "filter":{
                        "range":{
                            "price":{
                                "gte": min_price,
                                "lte": max_price
                            }
                        },
                        "range":{
                            "modelYear":{
                                "gte": min_model_year,
                                "lte": max_model_year
                            }
                        }
                    }
                }
        },
        "size": max_number_of_search_results
    }
            
else:
    elastic_query = {
        "query":{
                "bool":{
                    "must":[
                        {"match": {"location": city}},
                        {"match": {"vehicleType": vehicle_type}}],
                    "should":[
                        {"match": {"title":  query}},
                        {"match": {"description": query}}],
                    "filter":{
                        "range":{
                            "price":{
                                "gte": min_price,
                                "lte": max_price
                            }
                        },
                        "range":{
                            "modelYear":{
                                "gte": min_model_year,
                                "lte": max_model_year
                            }
                        }
                    }
                }
        },
        "size": max_number_of_search_results
    }

#execute query
res = es.search(index="simple", body=elastic_query)

#print result
print("Got " + str(res['hits']['total']) + " hits")
print("Displaying top " + str(max_number_of_search_results) + " documents\n")
for hit in res['hits']['hits']:
    #print(hit);
    print("SCORE:\t\t" + str(hit["_score"]))
    print("ID:\t\t" + str(hit["_source"]["id"]))
    print("TITLE:\t\t" + str(hit["_source"]["title"]))
    print("DATE:\t\t" + str(hit["_source"]["date"]))
    print("LOCATION:\t" + str(hit["_source"]["location"]))
    print("PRICE:\t\t" + str(hit["_source"]["price"]))
    print("SELLER:\t\t" + str(hit["_source"]["sellerName"]))
    print("MODEL YEAR:\t" + str(hit["_source"]["modelYear"]))
    print("VEHICLE TYPE:\t" + str(hit["_source"]["vehicleType"]))
    print("URL:\t\t" + str(hit["_source"]["url"]))
    print("DESCRIPTION:\n" + str(hit["_source"]["description"]))
    print();
