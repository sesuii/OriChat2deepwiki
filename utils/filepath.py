import datetime,time,os,json
from utils import constant
def read_file(path):
    with open(path, encoding='utf-8') as f:
        res = f.read()
        return res

def write_file(path, str):
    with open(path, "w") as f:
        f.write(str)


def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)  # 读取 JSON 并返回字典

def write_json(path, data):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file)  # 美化输出



def add_log( log_item):
   with open(constant.logfilePath, "a", encoding="utf-8") as file:
        json.dump(log_item, file)  # 美化输出
    # with open(path, "a") as logfile:
    #     logfile.write(log_item)

def initoutput():
    if not os.path.exists(constant.savedir):
        os.makedirs(constant.savedir) 
        write_json(constant.pagePath,[
            # {
            #     'isFinished':False,
            #     'modules':[
            #         {'isFinished':False,'index':0}, {'isFinished':False,'index':1}, {'isFinished':False,'index':2}
            #     ],'index':0
            # },
            #  {
            #     'isFinished':False,
            #     'modules':[
            #         {'isFinished':False,'index':0}, {'isFinished':False,'index':1}, {'isFinished':False,'index':2}
            #     ],'index':1
            # }
            
            
            ])
        write_json(constant.transitionPath,[])
        write_file(constant.logfilePath,'')

def readoutput():
    return [read_json(constant.pagePath),read_json(constant.transitionPath)]

def writeoutput(pages,links):
        write_json(constant.pagePath,pages)
        write_json(constant.transitionPath,links)

def get_timestamp():
    timestamp = datetime.datetime.fromtimestamp(
        int(time.time())).strftime("%Y-%m-%d-%H-%M-%S")
    res = {}

    basefile = constant.savedir + timestamp
    res['savedir'] = constant.savedir

    res['imgpath'] = basefile+'.png'
    res['xmlpath'] = basefile+'.xml'
    res['jsonpath'] = basefile+'.json'
    res['elementpath'] = basefile+'-element.json'
    res['timestamp'] = timestamp

    return res
