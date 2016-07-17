__author__ = 'Prateek'

import os
from hashlib import md5
from collections import deque

class NoSuchDirectory(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

class Crawler:
    def __init__(self, src_dir, force_crawl = False):
        self.src_dir = src_dir
        self.file_index = []
        self.dir_name_hash = ""
        if not os.path.isdir(src_dir):
            raise NoSuchDirectory("No such directory exists")

        self.dir_name_hash = md5(self.src_dir.rstrip(os.path.sep).encode("utf-8")).hexdigest()

        #temp dir for the dump files
        dump_dir = os.path.join(os.getcwd(), ".dump")
        output_file = os.path.join(dump_dir, self.dir_name_hash + ".txt") #<md5>.txt

        if (os.path.isfile(output_file) == False) or (force_crawl == True):
            if not os.path.exists(dump_dir):
                os.mkdir(dump_dir)
            self.bfs()
            self.write_to_file(output_file)
        else:
            print ("The index of the directory already exists")
            ch = input("Do you want to re-index the path (Y/N) : ")
            if ch.lower() in ("y", "yes"):
                self.bfs()
                self.write_to_file(output_file)

    def bfs(self):
        q = deque()
        q.append(self.src_dir)

        while len(q) != 0:
            path = q.pop()
            try:
                dirs = os.listdir(path)
            except:
                #path not accessible
                #ignoring this path
                continue

            for d in dirs:
                if d[0] == ".":
                    #temp or hidden folders
                    continue
                abs_path = os.path.join(path, d)
                if os.path.isdir(abs_path):
                    q.append(abs_path)
                else:
                    self.append_to_index(abs_path)

    def append_to_index(self, file_name):
        self.file_index.append(file_name)

    def write_to_file(self, output_file):
        with open(output_file, "w") as f:
            f.write("\n".join(f for f in self.file_index))

if __name__ == "__main__":
    c = Crawler("C:\\users\\prateek\\desktop\\code\\")