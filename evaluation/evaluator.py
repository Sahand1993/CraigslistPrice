import json
import statistics
import sys
sys.path.append('../elastic')
import searcher as my_searcher

while True:
        user_input = input("Choose to evaluate SEARCH ENGINE [s] or FILTERS [f]: ")
        if user_input=="s":
                file_name = "evaluation_manual_labeling.txt"
                break
        elif user_input=="f":
                file_name = "evaluation_manual_labeling_filter_test.txt"
                break

every_precision = []
every_recall = []
every_min_price_percentage_difference = []
every_max_price_percentage_difference = []
every_average_price_percentage_difference = []
every_median_price_percentage_difference = []

with open(file_name, encoding="utf8") as f:
        lines = f.read().splitlines()
        f.close()
        
number_of_rows = len(lines)
row = 0

#Execute each test query and compare the returned documents with the manual labeling
#regarding precision, recall and price statistics.
while row < number_of_rows:
        query = lines[row].split(':')[-1]
        model_years = lines[row+1].split(':')[-1]
        model_years = model_years.split('-')
        min_model = model_years[0]
        max_model = model_years[-1]
        loc = lines[row+2].split(':')[-1]
        vehicle = lines[row+3].split(':')[-1]
        subset_ids = lines[row+4].split(':')[-1]
        subset_ids = subset_ids.split('-')
        start_id = int(subset_ids[0])
        end_id = int(subset_ids[-1])
        relevant_ids = lines[row+5].split(':')[-1]
        if relevant_ids != "none":
                relevant_ids = list(map(int, relevant_ids.split(',')))
        else:
                relevant_ids = []
        somewhat_relevant_ids = lines[row+6].split(':')[-1]
        #We choose to classify somewhat relevants IDs as relevant.
        if somewhat_relevant_ids != "none":
                somewhat_relevant_ids = list(map(int, somewhat_relevant_ids.split(',')))
                relevant_ids = relevant_ids + somewhat_relevant_ids
        row += 8

        prices = []
        f_in = open("../dataset/motorcycles_python.json", "r", encoding='utf-8')
        doc_lines = f_in.readlines()
        f_out = open("subsets/"+str(start_id)+"_"+str(end_id)+".json", "w", encoding='utf-8')
        for line in doc_lines:
                json_obj = json.loads(line)["_source"]
                if start_id<=json_obj["id"]<=end_id:
                        f_out.write(line)
                if json_obj["id"] in relevant_ids:
                        prices.append(json_obj["price"])
        f_in.close()
        f_out.close()
        
        prices = list(map(int, prices))
        prices.sort()
        min_price_manual = prices[0]
        max_price_manual = prices[-1]
        average_price_manual = statistics.mean(prices)
        median_price_manual = statistics.median(prices)

        #Create index for the subset of documents.
        my_searcher.PATH_TO_DATASET = "subsets/"+str(start_id)+"_"+str(end_id)+".json"
        searcher = my_searcher.Searcher()

        #Execute query and search for documents in the subset.
        if query=="none" and min_model=="all" and loc=="all" and vehicle=="all":
                returned_docs = searcher.similar()
                price_stats = searcher.price()
        elif query!="none" and min_model=="all" and loc=="all" and vehicle=="all":
                returned_docs = searcher.similar(query)
                price_stats = searcher.price(query)
        elif query=="none" and min_model!="all" and loc=="all" and vehicle=="all":
                returned_docs = searcher.similar(min_model_year=int(min_model), max_model_year=int(max_model))
                price_stats = searcher.price(min_model_year=int(min_model), max_model_year=int(max_model))
        elif query=="none" and min_model=="all" and loc!="all" and vehicle=="all":
                returned_docs = searcher.similar(location=loc)
                price_stats = searcher.price(location=loc)
        elif query=="none" and min_model=="all" and loc=="all" and vehicle!="all":
                returned_docs = searcher.similar(vehicle_type=vehicle)
                price_stats = searcher.price(vehicle_type=vehicle)
        elif query!="none" and min_model!="all" and loc=="all" and vehicle=="all":
                returned_docs = searcher.similar(query, min_model_year=int(min_model), max_model_year=int(max_model))
                price_stats = searcher.price(query, min_model_year=int(min_model), max_model_year=int(max_model))
        elif query!="none" and min_model=="all" and loc!="all" and vehicle=="all":
                returned_docs = searcher.similar(query, location=loc)
                price_stats = searcher.price(query, location=loc)
        elif query!="none" and min_model=="all" and loc=="all" and vehicle!="all":
                returned_docs = searcher.similar(query, vehicle_type=vehicle)
                price_stats = searcher.price(query, vehicle_type=vehicle)
        elif query=="none" and min_model!="all" and loc!="all" and vehicle=="all":
                returned_docs = searcher.similar(min_model_year=int(min_model), max_model_year=int(max_model), location=loc)
                price_stats = searcher.price(min_model_year=int(min_model), max_model_year=int(max_model), location=loc)
        elif query=="none" and min_model!="all" and loc=="all" and vehicle!="all":
                returned_docs = searcher.similar(min_model_year=int(min_model), max_model_year=int(max_model), vehicle_type=vehicle)
                price_stats = searcher.price(min_model_year=int(min_model), max_model_year=int(max_model), vehicle_type=vehicle)
        elif query=="none" and min_model=="all" and loc!="all" and vehicle!="all":
                returned_docs = searcher.similar(location=loc, vehicle_type=vehicle)
                price_stats = searcher.price(location=loc, vehicle_type=vehicle)
        elif query!="none" and min_model!="all" and loc!="all" and vehicle=="all":
                returned_docs = searcher.similar(query, min_model_year=int(min_model), max_model_year=int(max_model), location=loc)
                price_stats = searcher.price(query, min_model_year=int(min_model), max_model_year=int(max_model), location=loc)
        elif query!="none" and min_model!="all" and loc=="all" and vehicle!="all":
                returned_docs = searcher.similar(query, min_model_year=int(min_model), max_model_year=int(max_model), vehicle_type=vehicle)
                price_stats = searcher.price(query, min_model_year=int(min_model), max_model_year=int(max_model), vehicle_type=vehicle)
        elif query!="none" and min_model=="all" and loc!="all" and vehicle!="all":
                returned_docs = searcher.similar(query, location=loc, vehicle_type=vehicle)
                price_stats = searcher.price(query, location=loc, vehicle_type=vehicle)
        elif query=="none" and min_model!="all" and loc!="all" and vehicle!="all":
                returned_docs = searcher.similar(min_model_year=int(min_model), max_model_year=int(max_model), location=loc, vehicle_type=vehicle)
                price_stats = searcher.price(min_model_year=int(min_model), max_model_year=int(max_model), location=loc, vehicle_type=vehicle)
        elif query!="none" and min_model!="all" and loc!="all" and vehicle!="all":
                returned_docs = searcher.similar(query, min_model_year=int(min_model), max_model_year=int(max_model), location=loc, vehicle_type=vehicle)
                price_stats = searcher.price(query, min_model_year=int(min_model), max_model_year=int(max_model), location=loc, vehicle_type=vehicle)
        else:
                system("Error")

        #Compare returned documents (and price statistics) from the search engine to the manual labeling.
        min_price_search_engine = price_stats["min_price"]
        max_price_search_engine = price_stats["max_price"]
        average_price_search_engine = price_stats["average_price"]
        median_price_search_engine = price_stats["median_price"]
        ret_docs = []
        true_positives = []
        for doc in returned_docs:
                ret_docs.append(doc["_source"]["id"])
                if doc["_source"]["id"] in relevant_ids:
                        true_positives.append(doc["_source"]["id"])
        precision = len(true_positives) / (len(ret_docs)*1.0)
        recall = len(true_positives) / (len(relevant_ids)*1.0)

        every_precision.append(precision)
        every_recall.append(recall)
        min_price_diff = (abs(min_price_search_engine-min_price_manual)/(abs(min_price_search_engine+min_price_manual)/2.0))*100
        every_min_price_percentage_difference.append(min_price_diff)
        max_price_diff = (abs(max_price_search_engine-max_price_manual)/(abs(max_price_search_engine+max_price_manual)/2.0))*100
        every_max_price_percentage_difference.append(max_price_diff)
        average_price_diff = (abs(average_price_search_engine-average_price_manual)/(abs(average_price_search_engine+average_price_manual)/2.0))*100
        every_average_price_percentage_difference.append(average_price_diff)
        median_price_diff = (abs(median_price_search_engine-median_price_manual)/(abs(median_price_search_engine+median_price_manual)/2.0))*100
        every_median_price_percentage_difference.append(median_price_diff)
        
        #Printing details about each result.
        print("Precision: "+str(precision)+" Recall: "+str(recall))
        print("Relevant Docs in Subset:", relevant_ids)
        print("Docs Returned by Search Engine:", ret_docs)
        print("True Positives:", true_positives)
        print("Minimum Price Manual: ", min_price_manual)
        print("Mininum Price Search Engine: ", min_price_search_engine)
        print("Maximum Price Manual: ", max_price_manual)
        print("Maximum Price Search Engine: ", max_price_search_engine)
        print("Average Price Manual: ", average_price_manual)
        print("Average Price Search Engine: ", average_price_search_engine)
        print("Median Price Manual: ", median_price_manual)
        print("Median Price Search Engine: ", median_price_search_engine, "\n")
        
#Printing summary of all results.
print("\nSUMMARIZED RESULT:")
print("Average Precision: "+str(statistics.mean(every_precision)))
print("Average Recall: "+str(statistics.mean(every_recall)))
print("Average Minimum Price Percentage Difference: "+str(statistics.mean(every_min_price_percentage_difference))+"%")
print("Average Maximum Price Percentage Difference: "+str(statistics.mean(every_max_price_percentage_difference))+"%")
print("Average Average Price Percentage Difference: "+str(statistics.mean(every_average_price_percentage_difference))+"%")
print("Average Median Price Percentage Difference: "+str(statistics.mean(every_median_price_percentage_difference))+"%")
