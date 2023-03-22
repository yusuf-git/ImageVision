# updates on 06-Oct-2020 08:05 PM, 11-Oct-2020 02:30 PM to 11:50 PM, 12-Oct-2020 02:00 AM #
import json
class net_analysis_report:
    def __init__(self, image, net_result, image_located_flag, failed_algos):  
        self.image = image
        self.net_result = net_result
        self.image_located_flag = image_located_flag
        self.failed_algos = failed_algos

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __repr__(self):  
        return "image:% s, net_result:% s, image_located_flag:% s, failed_algos:% s" % (self.image, self.net_result, self.image_located_flag, self.failed_algos)

    net_analysis_details_list = []


    def dump(self):
        return  {'image': self.image,
                 'net_result':self.net_result,
                 'image_located_flag':self.image_located_flag,
                 'failed_algos': self.failed_algos}


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        #if isinstance(o, Custom):
        #    return 'YES-RIGHT'
        return CustomEncoder(self, o)

