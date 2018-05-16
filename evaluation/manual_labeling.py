import json

min_id = 4243
max_id = min_id + 99

f_in = open("eval.json", "r", encoding='utf-8')
lines = f_in.readlines()

print("Displaying docs with ID: " + str(min_id) + "-" + str(max_id) + "\n")
number_of_objects = 0
for line in lines:
        json_obj = json.loads(line)["_source"]
        if min_id <= json_obj["id"] <= max_id:
                print("ID:\t\t" + str(json_obj["id"]))
                print("VEHICLE TYPE:\t" + str(json_obj["vehicleType"]))
                print("MODEL YEAR:\t" + str(json_obj["modelYear"]))
                print("LOCATION:\t" + str(json_obj["location"]))
                print("TITLE:\t\t" + str(json_obj["title"]))
                print("DESCRIPTION:\n" + str(json_obj["description"]))
                print();
                number_of_objects = number_of_objects + 1

f_in.close()
print("Displayed " + str(number_of_objects) + " objects.")
