import sys 
import os
import re
import neuprint as neu
import inquirer
import warnings
import json

# Global variables

global client, token, server, windows_dir_seperator, unix_dir_seperator, default_dset
server = 'https://neuprint.janelia.org'
token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InZmYndvcmtzaG9wLm5ldXJvZmx5MjAyMEBnbWFpbC5jb20iLCJsZXZlbCI6Im5vYXV0aCIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg2Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tWXFDN21NRXd3TlEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQU1adXVjbU5zaXhXZDRhM0VyTTQ0ODBMa2IzNDdvUlpfUS9zOTYtYy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3OTQwOTE4ODd9.ceg4mrj2o-aOhK0NHNGmBacg8R34PBPoLBwhCo4uOCQ"
default_dset = "hemibrain:v1.2.1"
client = neu.Client(server, dataset = default_dset, token = token)
windows_dir_seperator = "\\"
unix_dir_seperator = "/"

# OS_path_seperator

if os.name == "nt":
    seperator = windows_dir_seperator
else:
    seperator = unix_dir_seperator

# Choose dataset with checkbox in inquirer

def choose_dataset():

    path = os.path.dirname(os.path.realpath(__file__))
    os.makedirs(path + seperator + 'cache', exist_ok=True)
    try:
       choices =  list(neu.Client.fetch_datasets(client,reload_cache=False).keys())
       print(choices)
       if not os.path.isfile(path +seperator +'cache' + seperator + 'datasets.json'):
           with open(path +seperator +'cache' + seperator + 'datasets.json', 'w') as f:
               json.dump(choices, f, indent=2)
    except:
        warnings.warn(f"warning: unable to fetch datasets using defaults")
        if os.path.isfile(path +seperator +'cache' + seperator + 'datasets.json'):
            with open(path +seperator +'cache' + seperator + 'datasets','r') as f:
                choices = json.load(f)
        else :
            raise ValueError("no local datasets to choose")
    
    questions = [ inquirer.Checkbox('datasets', message="Choose dataset",choices = choices,),]
    answers = inquirer.prompt(questions)
    return answers

##########################################################################################
############################### Manager Class ############################################
##########################################################################################

class manager:

    def __init__(self, datasets=[], path = os.path.dirname(os.path.realpath(__file__))):
        self.datasets = datasets

        if not len(self.datasets):
            raise ValueError("datasets not specfied")

        for i in self.datasets:
            
            # create dataset dir
            if not self.__check_dir__(path + seperator + 'cache' + seperator + self._name_restrictions_(f'{i}')) or True :
                new_client = self.__set_client__(i)
                self.gen_dir(path + seperator + 'cache' + seperator + self._name_restrictions_(f'{i}'))
                self.gen_dir(path + seperator  + self._name_restrictions_(f'{i}'))
            
            # get all rois and create rois dirs
                all_rois = neu.queries.fetch_roi_hierarchy(include_subprimary=True, mark_primary=True, format='dict', client=new_client)
                self.gen_dir_sys(all_rois, path + seperator + self._name_restrictions_(f'{i}'))
            
            # get all neurons main types (how do we deal with other data sets
            # crate type directory
            # create subtypes directory
            # create neuron dir Id_type_sub_type
            # connectivity df both from fetch_neuron and fetch_adjacencies
            ...

    @classmethod
    def gen_dir(cls, directory):
        if not cls.__check_dir__(directory):
            os.makedirs(directory, exist_ok=True)
   
    @classmethod
    def gen_dir_sys(cls, dir_dict, root_directory):
        if not bool(dir_dict):
            return
        for p, q in dir_dict.items():
            next_directory = root_directory + seperator + cls._name_restrictions_(p)
            print(next_directory)
            cls.gen_dir(next_directory)
            cls.gen_dir_sys(q, next_directory)
    
    @classmethod 
    def __rsync__(cls):
        ...

    @classmethod
    def __set_client__(cls, dataset):
        return neu.Client(server, dataset=dataset, token=token) 

    @classmethod
    def __get_server_status__(cls):
        return neu.Client.fetch_server_info(client)

    @classmethod 
    def __version_dector__(cls):
        return neu.Client.fetch_db_version(client)

    @classmethod
    def __get_rois__(cls, dataset):
        return neu.queries.fetch_all_rois(client=cls.__set_client__(dataset))

    @classmethod 
    def __check_dir__(cls, directory_path):
        if os.path.exists(directory_path):
            return True
        else:
            return False
    
    @classmethod
    def _name_restrictions_(cls, name):
        #win = ['*',' " ', ' / ',  '<',  '>', ':', '|', '?', '\\']
        win1 = '["/<>:|?]'
        win2 = '[*]' 
        if os.name == "nt":
            name = re.sub(win1, "", name)
            name = re.sub(win2, "'", name)
        else:
            name = re.sub("[/]", "", name)
        return name

    @classmethod 
    def __check_file__(file_path):
        if os.path.isfile(file_path):
            return True
        else:
            return False

##########################################################################################
####################################### MAIN  ############################################
##########################################################################################


if __name__ == "__main__":
    
    home_dir = os.path.dirname(os.path.realpath(__file__))
    dataset = choose_dataset()
    #print(dataset['datasets'])
    manager(dataset['datasets'],path= home_dir)
