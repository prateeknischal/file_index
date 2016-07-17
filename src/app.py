__author__ = 'Prateek'

from utils import *
import http.server
import argparse

class App:
    def __init__(self, path, force_crawl = False):
        #build the index
        self.path = path

        print ("crawling the directories...")
        self.crawler = crawler.Crawler(path, force_crawl)
        self.dir_name_hash = self.crawler.dir_name_hash

        #build the ds
        print ("Init indexing...")
        self.build_ds = build_ds.BuildDS(index_file_name = self.dir_name_hash + ".txt",
                                               dump_file_name = self.dir_name_hash + "_dump.dmp")
        print ("Starting indexing of directories...")
        self.build_ds.begin()
        print ("Indexing and serializing done...")


        #start the server
        print ("Setting up the server...")
        server_handler.MyHandler.ds = self.build_ds
        httpd = http.server.HTTPServer(("localhost", 10250), server_handler.MyHandler)
        print ("server started at localhost:10250...!")
        httpd.serve_forever()

def test():
    App("C:\\Users\\prateek\\desktop\\", True)
if __name__ == "__main__":
    # test()
    parser = argparse.ArgumentParser()
    parser.add_argument("src", help = "The root dir for crawl")
    parser.add_argument("-f", "--force",
						action = "store_true" , dest = "force",
						default = False,
						help = "Force the crawler to index pre-indexed paths")
    args = parser.parse_args()
    App(args.src, args.force)
