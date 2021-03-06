__author__ = 'Prateek'

import http.server
import urllib.parse as urlparse
from utils import name_splitter

class MyHandler(http.server.BaseHTTPRequestHandler):
    # Copy of the data structure object
    ds = None

    def do_GET(self):
        resp = self.send_head()
        self.wfile.write(resp)


    def send_head(self):
        query_list = self.parse_path(self.path)
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        query_res = self.query_DS(query_list)
        response = "\n".join(str(x) for x in query_res)

        #if len(query_list):
        #    resp = ("\n".join("{}:{}".format(k, v) for k, v in query_list.items()) + "\n").encode("utf-8")
        #    self.wfile.write(resp)
        #else:
        #    resp = "Content Not available !".encode("utf-8")

        if len(response):
            ret = response.encode("utf-8")
        else:
            ret = "No such files found".encode("utf-8")

        self.send_header("Content-Length", len(ret))
        self.end_headers()
        return ret

    def parse_path(self, path):
        #get query params
        # /?param1=value1&params2=value2
        lst = path.split('?', 1)
        if len(lst) == 1:
            path = ""
            return {}
        else:
            path = lst[1]

        path = urlparse.unquote(path)
        query_list = {}

        for query in path.split('&'):
            k, v = map(str, query.split('='))
            query_list[k] = v
        return query_list

    @staticmethod
    def DS_OR(a, b):
        # This returns all the entries that are in both of the files
        # equivalent to intersection of 2 sets()
        setA = set(a)
        setB = set(b)
        res = [x for x in setA | setB]
        return res
    
    def query_DS(self, q):
        fname = q.get('fname', None)
        ext = q.get('ext', None)
        #dir = q.get('dir', None)
        if fname is None:
            return set()
        tok_list = name_splitter.split_file_name(fname)
        
        res_set = []
        if ext is None:
            #check in all the available file extensions
            for _ext in self.ds.avail_ext:
                for tok in tok_list:
                    res_set = MyHandler.DS_OR(res_set, self.ds.dt[_ext].get(tok, []))
        else:
            for tok in tok_list:
                # check in the dt[ext] dictionary for the file_names
                res_set = MyHandler.DS_OR(res_set, self.ds.dt[ext].get(tok, []))
            
        return res_set


if __name__ == "__main__":
    httpd = http.server.HTTPServer(("localhost", 9999), MyHandler)
    httpd.serve_forever()
