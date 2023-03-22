# updates on 06-Oct-2020 08:05 PM, 11-Oct-2020 02:30 PM to 11:50 PM, 12-Oct-2020 02:00 AM #
import json
class hang_issue_checker_data_model:
    def __init__(self, base_image, runtime_image, img_path, algo, expscore, original_score, result, msg):  
        self.base_image = base_image
        self.runtime_image = runtime_image
        self.img_path = img_path
        self.algo = algo
        self.expscore = expscore  
        self.original_score = original_score
        self.result = result
        self.msg = msg
    #image_match_outcome_dict = {}
    hang_issue_checker_result_list = []
    tmp_img_match_result_list = []

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self):  
        return "base_image:% s, runtime_image:% s, img_path:% s, algo:% s, exp-score:% s, orig-score:% s, result:% s, msg:% s" % (self.base_image, self.runtime_image, self.img_path, self.algo, self.expscore, self.original_score, self.result, self.msg)

    


    def dump(self):
        return  {'base_image': self.base_image,
                 'runtime_image':self.runtime_image,
                 'img_path':self.img_path,
                 'algo': self.algo,
                 'expscore': self.expscore,
                 'original_score': self.original_score,
                 'result':self.result,
                 'msg':self.msg}


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        #if isinstance(o, Custom):
        #    return 'YES-RIGHT'
        return CustomEncoder(self, o)

