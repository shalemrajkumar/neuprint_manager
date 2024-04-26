import sys 
import os
import neuprint as neu
import inquirer
import warnings
import json

#client token
client = neu.Client('https://neuprint.janelia.org',
                            token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InZmYndvcmtzaG9wLm5ldXJvZmx5MjAyMEBnbWFpbC5jb20iLCJsZXZlbCI6Im5vYXV0aCIsImltYWdlLXVybCI6Imh0dHBzOi8vbGg2Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tWXFDN21NRXd3TlEvQUFBQUFBQUFBQUkvQUFBQUFBQUFBQUEvQU1adXVjbU5zaXhXZDRhM0VyTTQ0ODBMa2IzNDdvUlpfUS9zOTYtYy9waG90by5qcGc_c3o9NTA_c3o9NTAiLCJleHAiOjE3OTQwOTE4ODd9.ceg4mrj2o-aOhK0NHNGmBacg8R34PBPoLBwhCo4uOCQ")
windows_dir_seperator = "\\"
unix_dir_seperator = "/"

if os.name == "nt":
    seperator = windows_dir_seperator
else:
    seperator = unix_dir_seperator

def choose_dataset():

    path = os.path.dirname(os.path.realpath(__file__))
    
    try:
       choices =  list(neu.Client.fetch_datasets(client,reload_cache=False).keys())
       print(choices)
       if not os.path.isfile(path +seperator +'datasets.json'):
           with open(path + seperator + 'datasets.json', 'w') as f:
               json.dump(choices, f, indent=2)
    except:
        warnings.warn(f"warning: unable to fetch datasets using defaults")
        if os.path.isfile( path +"seperator"+ 'datasets.json'):
            with open( path + seperator + 'datasets.json','r') as f:
                choices = json.load(f)
        else :
            raise ValueError("no local datasets to choose")
    
    questions = [ inquirer.Checkbox('datasets', message="Choose dataset",choices = choices,),]
    answers = inquirer.prompt(questions)
    return answers

class manager:

    def __init__(self, datasets=[]):
        self.datasets = datasets

        if len(self.datasets):
            raise ValueError("datasets not specfied")

        for i in dataset:

    
    def gen_dir(self, directory):
        if not cls.__check_dir__(directory) :
            os.makedirs(path + directory, exists_ok=True)
            

    @classmethod 
    def __rsync__(cls):
        ...

    @classmethod
    def __get_server_status__(cls):
        return neu.Client.fetch_server_info(client)

    @classmethod 
    def __version_dector__(cls):
        return neu.Client.fetch_db_version(client)

    @classmethod
    def__get_rois__(cls, dataset):


    @classmethod 
    def __check_dir__(directory):
        if os.path.exists(path + seperator + directory):
            return True
        else:
            return False

    def __file_sys__():
        ...


if __name__ == "__main__":
    choose_dataset()

