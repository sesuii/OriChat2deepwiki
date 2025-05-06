from utils import and_controller,eletree,filepath,gpt
import time
controller = and_controller.AndroidController()

# 添加启动页面
def initialize_pages(pages):
    act = exec_action()
    appinfo=act['appinfo']
    assets =act['assets']
    add_current_page(pages,appinfo,assets)


# 执行模块探索
def testModule(pages,links,pageIndex,moduleindex):
    page = pages[pageIndex]
    module = page['functional_modules'][moduleindex]
    todoList = module['todoList']
    steps = []
    if page['in_edges']:  steps.extend( links[page['in_edges'][0]] )# 取第一个入度边
    act = exec_steps(steps,pages)
    count =0
    interation = []

    while True:
        count += 1
        # 待测页面内进行探索
        # print(module)
        if len(todoList) == 0 or count>10:  
            module['isFinished'] = True
            return 
        
        if(module['test_plan']['type'] == 'Other'):
            gpt_act = gpt.askAction({  
                    **act['assets'],
                    'appActivity':act['appinfo'][1],
                    'appPackage':act['appinfo'][0],
                    'module':{
                        'module_name':module['module_name'],
                        'bounds':module['bounds'],
                        'interactive_elements':module['interactive_elements'],
                        'test_plan':module['test_plan'],
                    },
                'steps':convert_actions_to_string_array(steps+interation),
            })
            if(gpt_act== 'FINISH') :
                module['isFinished'] = True
                return 
            act = exec_action(gpt_act,act['assets']['jsonpath'])
        else :
            act = exec_action({"type":'tap','ele':{'index':todoList[0]}},page['page_config']['jsonpath'])
            if(not act) : 
                todoList.pop(0)
                return
        act['from'] = page['index']
        appinfo=act['appinfo']
        assets =act['assets']

        interation.append(act)

        if(not appinfo):
            todoList.pop(0)
            act['to'] = "outofApp"
            link = steps + interation
            page['out_edges'].append(len(links))
            links.append(link)
            module['isFinished'] = True
            return 

        topage = find_same_page(pages,{'appinfo': appinfo, 'assets': assets})

        if(topage == -1):   #发现新页面
            current_page = add_current_page(pages,appinfo,assets)
            act['to'] = current_page['index']
            link = steps + interation
            page['out_edges'].append(len(links))
            current_page['in_edges'].append(len(links))
            links.append(link)
            if(module['test_plan']['type'] != 'Other'):todoList.pop(0)

            return 

        elif(topage['index'] != page['index']):  #探索到旧页面
            current_page = topage
            act['to'] = current_page['index']
            link = steps + interation
            page['out_edges'].append(len(links))
            current_page['in_edges'].append(len(links))
            links.append(link)
            if(module['test_plan']['type'] != 'Other'): todoList.pop(0)
            return 

        elif(topage['index'] == page['index']): #原页面
            if(module['test_plan']['type'] != 'Other'):todoList.pop(0)
            act['to'] = page['index']

        

               
            
               

            

# 保存当前页面的 UI 信息（XML、截图、JSON）
def save_page_state():
    assets = filepath.get_timestamp()
    appinfo = controller.get_info()
    controller.get_xml(assets['xmlpath'])
    controller.get_screenshot(assets['imgpath'])
    filepath.write_json(assets['jsonpath'],eletree.xmltojson(assets['xmlpath']))
    return  appinfo,assets
    
# 解析当前页面并添加到 `pages` 列表
def add_current_page(pages,appinfo,assets):
    # 组织页面配置数据
    page_config = {
        'xmlpath':assets['xmlpath'],
        'imgpath':assets['imgpath'],
        'jsonpath':assets['jsonpath'],
        'appActivity':appinfo[1],
        'appPackage':appinfo[0],
    }
    # 通过 GPT 解析页面功能模块
    ret = gpt.askPage(page_config)
    
    # 处理功能模块信息
    for index,module in enumerate(ret['functional_modules']):
        module['index'] = index
        module['isFinished'] = False
        module['todoList'] = []
        if(module['test_plan']['type'] == 'Sequential Click'):
            module['todoList'].extend(module['interactive_elements'])
        elif(module['test_plan']['type'] == 'Random Click'):
            module['todoList'].append(module['interactive_elements'][0])
        else:
            module['todoList'].append('others')
    for category, elements in ret['representative_ui_elements'].items():
        eles = []
        for idx in elements:
            node = eletree.findNode(page_config['jsonpath'],idx)
            eles.append(node)
        ret['representative_ui_elements'][category] = eles

    current_page = {
        'index':len(pages),
        'isFinished':False,
        'page_config':page_config,
        'out_edges': [],  # 出度：当前页面 → 其他页面
        'in_edges': [],  # 入度：其他页面 → 当前页面
        **ret}
    # 添加到 `pages` 列表
    pages.append(current_page)
    return current_page
    




def exec_steps(steps,pages=None):
    controller.stop_app()
    controller.start_app()
    time.sleep(3)
    ret = ''
    for step in steps:
        ret = exec_action(step,pages[step['from']]['page_config']['jsonpath'])
    return ret
        

def exec_action(action=None,jsonpath=None):
    ret = {}

    if(not action):
        controller.stop_app()
        controller.start_app()
        time.sleep(3)

    
    elif(action['type'] == 'tap'):
       
        node = eletree.findNode(jsonpath,action['ele']['index'])
        if not node : return None
        bounds = node['bounds'].strip("[]")
        left_top, right_bottom = bounds.split("][")
        left, top = map(int, left_top.split(","))
        right, bottom = map(int, right_bottom.split(","))
        controller.tap((left, top), (right, bottom))
        time.sleep(3)
        ret = {
            **ret,
            **action,
            'type':'tap',
            'ele':node,
        }
    elif(action['type'] == 'input'):
        controller.text(action['msg'])
        time.sleep(3)
        ret = {
            **ret,
            **action,
            'type':'input',
        }

    appinfo,assets = save_page_state()
    return {
            **ret,
            'appinfo':appinfo,
            'assets':assets
            }


def find_same_page(pages,currentPage):

    for page in pages:
        results = []
        matchresults = []
        if(page['page_config']['appActivity'] == currentPage['appinfo'][1]):
            for category, elements in page['representative_ui_elements'].items():
                for element in elements:
                    node = eletree.findNode(currentPage['assets']['jsonpath'], element['index'])
                    if (node and matches_node(node,element)) : matchresults.append(node)
                    results.append(node)
            if(len(results) == len(matchresults)): return page
            print(results)
    return -1


def matches_node(node, flag):

    ui = flag
    # 检查unique_identifier
    if 'resource-id' in ui:
        if node.get('resource-id') != ui['resource-id']:
            return False

    if 'class' in ui:
        if node.get('class') != ui['class']:
            return False
         # 检查class
    if 'text' in ui:
        if node.get('text') != ui['text']:
            return False
             # 检查class
    if 'content' in ui:
        if node.get('content') != ui['content']:
            return False

    if  'content-desc' in ui:
        if node.get('content-desc') != ui['content-desc']:
            return False

    # 检查index
    if 'index' in ui:
        if node.get('index') != ui['index']:
            return False

    # 如果所有存在的属性都匹配，则返回True
    return True


def convert_actions_to_string_array(actions):
    result=[]
    for i, action in enumerate(actions):
        action_type = action.get("type")
        letter=''
        if(action.get("msg")):
            letter = action['msg']
        else:
            if action.get('ele').get('text'):
                letter += action.get('ele').get('text') +' '
            if action.get('ele').get('resource-id'):
                letter += action.get('ele').get('resource-id') +' '
            if action.get('ele').get('class'):
                letter += action.get('ele').get('class')+ ' '
            if action.get('ele').get('content-desc'):
                letter += action.get('ele').get('content-desc')+' '
        result.append(f"{action_type}({letter})")
    return result

