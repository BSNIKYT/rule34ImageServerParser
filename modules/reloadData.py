import os
import json

if str(os.name) == "nt":dir_pref = "\\"
else:dir_pref = "/"

def reload_file_statistics(working_directory):
    statictics_file_name = 'statistics.json'
    if not os.path.exists(working_directory + dir_pref + statictics_file_name):
        q = []
        json.dump(q, open(statictics_file_name,'w'), indent=4, default=list)
        data_load=json.loads(open(statictics_file_name,'r').read())
    else:
        data_load=json.loads(open(statictics_file_name,'r').read())
    return data_load

def reload_file_config(working_directory):
    statictics_file_name = 'config.json'
    if not os.path.exists(working_directory + dir_pref + statictics_file_name):
        q = []
        GuardVal = True
        BlockedTags = [
            "furry",
            "futanari",
            "erect penis",
            "anthro",
            "presenting_anus",
            "presenting_penis",
            "muscular_male",
            "2boys",
        ]



        q.append({'GuardOnline': GuardVal,
                  'GuardBlockedTags': BlockedTags})
        json.dump(q, open(statictics_file_name,'w'), indent=4, default=list)
        data_load=json.loads(open(statictics_file_name,'r').read())



    else:
        data_load=json.loads(open(statictics_file_name,'r').read())
    return data_load

