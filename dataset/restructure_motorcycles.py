## restructures motorcycle data on the initial form to a form that fits the Elasticsearch Python library.

import json

f_in = open("motorcycles.json", "r")
f_out = open("motorcycles_python.json", "w")
lines = f_in.readlines()

length = len(lines)
i = 0

while i+1 < length:
	action = lines[i]
	source = lines[i+1]
	json_obj = json.loads(action)["index"]
	json_obj["_source"] = json.loads(source)
	f_out.write(json.dumps(json_obj, sort_keys=True, indent=4)+"\n")
	i += 2

f_in.close()
f_out.close()