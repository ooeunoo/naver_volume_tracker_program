# -*- coding: utf-8 -*-

import json
def extract_json_list(input_string):
    json_list = []
    start_index = input_string.find('[')
    end_index = input_string.find(']')
    if start_index != -1 and end_index != -1:
        json_str = input_string[start_index:end_index+1]
        try:
            json_list = json.loads(json_str)
        except ValueError as e:
            print("Error:", e)
    return json_list
