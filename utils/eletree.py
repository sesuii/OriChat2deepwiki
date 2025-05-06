import xml.etree.ElementTree as ET
import utils.filepath as path
import json

def findContent(ele):
    res = ''
    if((ele.attrib.get('resource-id'))):
        res += ele.attrib.get('resource-id') + ' '
    if((ele.attrib.get('text'))):
        res += ele.attrib.get('text') + ' '
    if((ele.attrib.get('content-desc'))):
        res += ele.attrib.get('content-desc') + ' '
    if((ele.attrib.get('class'))):
        res += ele.attrib.get('class').replace('android.widget.','').replace('android.view.','') + ' '

    for key in ele:
        res += findContent(key)
    return res


def addELE(tree ,arr, ele, index):
    treeitem = {}
    arritem = {}
    tree.append(treeitem)
    arr.append(arritem)
    treeitem['bounds'] = arritem['bounds'] =ele.attrib.get('bounds')
    treeitem['index'] = arritem['index']  = index
    if(ele.attrib.get('clickable') == 'true'):
        treeitem['clickable'] = arritem['clickable'] = ele.attrib.get('clickable')
        # treeitem['content'] = arritem['content'] = findContent(ele)
        # return
    if((ele.attrib.get('text'))):
        treeitem['text'] = arritem['text'] = ele.attrib.get('text')
    if((ele.attrib.get('resource-id'))):
        treeitem['resource-id'] = arritem['resource-id'] = ele.attrib.get('resource-id')
    if((ele.attrib.get('class'))):
        treeitem['class'] = arritem['class'] = ele.attrib.get('class').replace('android.widget.','').replace('android.view.','')
    if((ele.attrib.get('content-desc'))):
        treeitem['content-desc'] = arritem['content-desc']= ele.attrib.get('content-desc')
    for key in ele:
        if(treeitem.get('children') == None):
            treeitem['children'] = []
        addELE(treeitem['children'],arr, key, index+'-'+key.get('index'))


def findele(arr,index):
    for ele in arr:
        if(ele.get('index') == index):
            return ele
    return None
        
def findNode(jsonfilepath,index):
    arr = json.loads(path.read_file(jsonfilepath))['array']
    container =  findele(arr,index)
    if (container):
        return container
    else:
        return None
    

def findContainerByIndex(srcfile,index):
    jsonele = json.loads(path.read_file(srcfile)) 
    container =  findele(jsonele[0],index)
    if (container):
        bounds = container.get('bounds')
        x1 = bounds[1:-1].split("][")[0].split(",")[0]
        y1 = bounds[1:-1].split("][")[0].split(",")[1]
        x2 = bounds[1:-1].split("][")[1].split(",")[0]
        y2 = bounds[1:-1].split("][")[1].split(",")[1]
        w = str(int(x2)-int(x1))
        h = str(int(y2)-int(y1))
        res = index
        if(container.get('resource-id')):
            res+=' '+ container.get('resource-id')
        if(container.get('class') ):
            res += ' '+ container.get('class') 
        res += ' ' + w + ' ' + h
        return res
    else:
        return None



def xmltojson(path):
    tree = []
    array = []
    try:
        root = ET.parse(path).getroot()[0]
        addELE(tree,array, root ,root.get('index'))
        return {'tree': tree,'array':array}
    except:

        return 'error'
