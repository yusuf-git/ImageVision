# Created on 15-Dec-2021 12:40 AM #
import json
class RT_negative_cond_result:
    def __init__(self, runtime_img, result):  
        self.runtime_img = runtime_img
        self.result = result
    result_list = []
    

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self):  
        return "runtime_img:% s, result:% s" % (self.runtime_img, self.result)


    def dump(self):
        return  {'runtime_img':self.runtime_img,
                 'result':self.result }


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return CustomEncoder(self, o)

