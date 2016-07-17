__author__ = 'Prateek'

import os
import pickle
import utils.name_splitter

class BuildDS:
    """
	Reads from the indexed file and converts build a dictionary
	based on the filenames as keys and the values being the list of
	locations where the filename was found
	"""

    def __init__(self, index_file_name, dump_file_name):
        self.index_file_name = index_file_name;
        self.dump_file_name = dump_file_name
        self.dt = {}
        self.avail_ext = []

    def extract_file_names(self):
        dump_dir = os.path.join(os.getcwd(), ".dump")
        with open(os.path.join(dump_dir, self.index_file_name), "r") as fp:
            for line in fp:
                self.update_ds(line)
                
    def update_ds(self, file_name):
        fname = file_name.rstrip("\n")
        tmp, ext = os.path.splitext(fname) #extension of the file with a '.[ext]' eg '.py'
        ext = ext.lstrip('.') # remove the '.' if the extension has one
        
        d = os.path.basename(fname)
        path = file_name[: -len(d) - 1]
        tok_list = utils.name_splitter.split_file_name(d)
        # TODO reduce memory print by mapping the path to numbers as they are repetitve
        for token in tok_list:
            #check if the extension is present in the dict
            if self.dt.get(ext, None) is None:
                self.dt[ext] = {}

            # find the token if it exists in the 'ext' dict
            if self.dt[ext].get(token, None) is None:
                # If does not exist then add a list with file_name as entry
                self.dt[ext][token] = [fname]
            else:
                # If found then just append the file_name in the current list of token
                self.dt[ext][token].append(fname)
            
    def serialize_dt(self):
        dir_path = os.path.join(os.getcwd(), ".dump")
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        print ("serialize file " + os.path.join(dir_path, self.dump_file_name))
        with open(os.path.join(dir_path, self.dump_file_name), "wb") as fp:
            pickle.dump(self.dt, fp)

    def check_dump_file(self):
        d = os.getcwd()
        d = os.path.join(d, ".dump")

        if os.path.exists(d):
            #dump dir exists
            #load the db from it when not forced to crawl
            if os.path.isfile(self.dump_file_name):
                with open(os.path.join(d, self.dump_file_name), "rb") as fp:
                    self.dt = pickle.load(fp)
                return True
            else:
                return False
        return False
    
    def begin(self):
        if not self.check_dump_file():
            self.extract_file_names()
            self.serialize_dt()
        #load the list of file extensions available
        self.avail_ext = self.dt.keys()
