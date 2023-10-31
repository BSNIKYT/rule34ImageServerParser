import os
import json
from modules.reloadData import reload_file_statistics
from modules.reloadData import reload_file_config

black = "\033[30m" 
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
violet = "\033[35m"
turquoise = "\033[36m"
white = "\033[37m"
st = "\033[37"

if str(os.name) == "nt":dir_pref = "\\"
else:dir_pref = "/"


class Guard():
    def __init__(self, logger):
        self.logger = logger
        self.logger.info('[Guard] module has beel successfully loaded.')
        self.config_data = reload_file_config(os.getcwd())[0]
        self.online_val = self.config_data['GuardOnline']
        self.BlockedTags= self.config_data['GuardBlockedTags']
        self.logger.info(f"[Guard] {'='*11}")
        self.logger.info(f'[Guard] Online: {self.online_val}')
        self.logger.info(f"[Guard] {'-'*8}")
        for tag in self.config_data['GuardBlockedTags']:
            self.logger.info(f'[Guard] Tag: {tag}')
        self.logger.info(f"[Guard] {'='*11}")
        if self.online_val == True:
            print(f"{green}[+] GuardStatus: {self.online_val}")
            print(f"[+] {white}Number of blocked tags: {blue}{len(self.config_data['GuardBlockedTags'])}{white}")
        else:print(f"{red}[-] GuardStatus: {self.online_val}{white}")



        if self.online_val == True:
            self.guardON = True
        else:self.guardON = False
    
    def GuardCheck(self, tags, file_url, _id):
        if self.config_data['GuardOnline'] == True:
            if type(tags) == list:
                for tag in tags:
                    if tag in self.BlockedTags:
                        self.logger.warning(f'''{'='*10}- [FIND] -{'='*10}''')
                        self.logger.warning(f'[Guard] -[ A blacklisted tag was found: {tag}')
                        self.logger.warning(f'[Guard] -[ File Url: {file_url}')
                        self.logger.warning(f'[Guard] -[ ID: {_id}')
                        self.logger.warning(f'''{'='*10}-        -{'='*10}''')
                        print(f'{red}[Guard]: A blacklisted tag was found: {tag}{white}')
                        return False
                return True
        else:return True

       







class GlobalTagsInfo():
    tagsGlobal = []

    def __init__(self, logger):
        self.logger = logger
    
    def ch_new_tags(self, input_tags):
        if type(input_tags) != list:
            input_tags = input_tags.split(' ')
        for new_or_old_tags in input_tags:
                if new_or_old_tags not in self.tagsGlobal:
                    self.tagsGlobal.append(input_tags)
    
    def FrSTRtoList(self, input_tags):
        tagsOut = []
        self.data_load = self.input_tags
        for i in range(0,len(data_load)):
            zn = data_load[i][0]
            if zn not in tagsOut:
                zn = zn.replace(' ','')
                for tag in zn.split('\n'):
                    if tag != '':
                        if tag not in tagsOut:
                            tagsOut.append(str(tag))
        return tagsOut
    

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
        with open("GlobalTagsInput.json", "w") as outfile:json.dump(tagsOut, outfile, indent=4)
        self.logger.info('[GlobalTagsInfo] File created [GlobalTagsInput.json]')
        print('File created [GlobalTagsInput.json]')
    
        




class Statistics():
   
    def __init__(self, working_dir, logger):
        self.logger = logger
        self.logger.info('[Statistics] module has beel successfully loaded.')
        self.logger.info(f"[Statistics] {'='*11}")
        self.working_directory = working_dir
        self.logger.info(f'[Statistics] Working Directory: {self.working_directory}')
        self.data_load = reload_file_statistics(self.working_directory)
        self.logger.info(f'[Statistics] Data loaded successfully.')
        self.data_stats = self.data_load
    

    def statistics_format_function_ok(self, data):
        self.data_stats.append(data)

    def statistics_format_function_error(self, data):
        self.data_stats.append(data)

    def writeStats(self):
        with open("statistics.json", "w") as outfile:json.dump(self.data_stats, outfile, indent=4)
        self.logger.info('[Statistics] File created [statistics.json]')
        print('File created [statistics.json]')


if __name__ == "__main__":
    print(Guard())