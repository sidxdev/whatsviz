import sys
import json
import os
import re
import pandas as pd


pattern = '^(\\d\\d\\/\\d\\d\\/\\d\\d), (\\d?\\d:\\d\\d ..) - (.+?): (.*)$'

args = sys.argv
if(len(args) != 3):
    print('Provide the input/output chat file as a command line argument!')
    sys.exit()


file_in = args[1]
file_out = args[2]

with open(file_in, "r", encoding="utf8") as fh:
    lines = fh.readlines()

parsed_input = []

for line in lines:
    matches = re.findall(pattern, line)
    if(len(matches) > 0):
        converted_line = {
            "date": matches[0][0],
            "time": matches[0][1],
            "sender": matches[0][2],
            "text": matches[0][3]
        }
        parsed_input.append(converted_line)
    else:
        parsed_input[len(parsed_input) - 1]['text'] += line

df = pd.DataFrame(parsed_input)
summary = df.groupby(['sender']).size().reset_index()
summary.columns = ['sender', 'count']
print(summary)

output = {
    "summary": json.loads(summary.to_json(orient='records'))
}

out_file = open(file_out, "w")
json.dump(output, out_file, indent=4, sort_keys=False)
out_file.close()

# os.remove(file_in)