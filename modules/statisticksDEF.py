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

def add_new_session(old_data):
    pass



class GlobalTagsInfo():
    tagsGlobal = []
    
    def ch_new_tags(self, input_tags):
        if type(input_tags) != list:
            input_tags = input_tags.split(' ')
        for new_or_old_tags in input_tags:
                if new_or_old_tags not in self.tagsGlobal:
                    self.tagsGlobal.append(input_tags)
    

    def writeTags(self):
        data_load = self.tagsGlobal
        tagsOut = []
        for i in range(0,len(data_load)):
            zn = data_load[i][0]
            if zn not in tagsOut:
                zn = zn.replace(' ','')
                for tag in zn.split('\n'):
                    if tag != '':
                        if tag not in tagsOut:
                            tagsOut.append(str(tag))
        with open(f"GlobalTagsInput.json", "w") as outfile:json.dump(tagsOut, outfile, indent=4)
        print('File created [GlobalTagsInput.json]')
    
        




class Statistics():
   
    def __init__(self, working_dir):
        self.working_directory = working_dir
        self.data_load = reload_file_statistics(self.working_directory)
        self.data_stats = self.data_load
    

    def statistics_format_function_ok(self, data):
        self.data_stats.append(data)
        pass

    def statistics_format_function_error(self, data):
        self.data_stats.append(data)
        pass

    def writeStats(self):
        with open(f"statistics.json", "w") as outfile:json.dump(self.data_stats, outfile, indent=4)
        print('File created [statistics.json]')