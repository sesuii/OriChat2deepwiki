import openai
import base64

import time
import json
import re

from utils import prompt_page, filepath, constant,prompts,prompt_fun


openai.api_key = constant.api_key


def image_b64(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()


def parseObject(rsp):
    msg = rsp["choices"][0]['message']['content']
    # msg = rsp
    resultjson = json.loads(msg[msg.find('{'):msg.rfind('}')+1])

    return resultjson


def ask_gpt4v(messages, model="gpt-4o-mini"):
    start = int(time.time())
    print('ask.........................')
    response = openai.ChatCompletion.create(
        model=model,
        frequency_penalty=0,
        presence_penalty=0,
        messages=messages,
        max_tokens=1024*8,
        temperature=0
    )
    period = int(time.time()) - start
    input_cost = response['usage']['prompt_tokens']*0.15/1000000
    output_cost = response['usage']['completion_tokens']*0.06/1000000
    print("time: "+str(period))
    print("input_cost: "+str(input_cost)+'$')
    print("output_cost: "+str(output_cost)+'$')
    print(response)
    return (response)

def askPage(viewObj):
    imgpath = viewObj['imgpath']
    jsonpath = viewObj['jsonpath']
    App_Information = {
        'appActivity': viewObj['appActivity'],
        'appPackage': viewObj['appPackage'],
        'appIntro': filepath.read_file(constant.info)
    }

    messages1 = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_page.get_functional_modules
                },
                {
                    "type": "text",
                    "text": f"\
                            - xml:\t{filepath.read_json(jsonpath)['tree']} \n\n \
                            - information:\t{App_Information}\n\n \
                        ",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64(imgpath)}","detail": "low",},
                    
                },
            ]
        }
    ]

    messages2 = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_page.get_representative_ui_elements
                },
                {
                    "type": "text",
                    "text": f"\
                            - xml:\t{filepath.read_json(jsonpath)['tree']} \n\n \
                            - information:\t{App_Information}\n\n \
                        ",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64(imgpath)}","detail": "low",},
                    
                },
            ]
        }
    ]
    

    rsp1 = ask_gpt4v(messages1)
    rsp2 = ask_gpt4v(messages2)

    filepath.add_log( {"response": rsp1, "request": {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_page.get_functional_modules
                },
                {
                    "type": "text",
                    "text": f"\
                            - xml:\t{(jsonpath)} \n\n \
                            - information:\t{App_Information}\n\n \
                        ",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{(imgpath)}","detail": "low",},
                    
                },
            ]
        }} )
    filepath.add_log( {"response": rsp2, "request": {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt_page.get_representative_ui_elements
                },
                {
                    "type": "text",
                    "text": f"\
                            - xml:\t{(jsonpath)} \n\n \
                            - information:\t{App_Information}\n\n \
                        ",
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{(imgpath)}","detail": "low",},
                    
                },
            ]
        }} )

    
    return {**parseObject(rsp1),**parseObject(rsp2)}

def askAction( viewObj):

    App_Information = {
        'appActivity': viewObj['appActivity'],
        'appPackage': viewObj['appPackage'],
        'appIntro': filepath.read_file(constant.info)
    }

    target = viewObj['module']
    steps = viewObj['steps']
    messages = [
        {
            "role": "user",
            "content": [
                    {
                        "type": "text",
                        "text": prompt_page.get_action
                    },
                {
                        "type": "text",
                        "text": f"\
                            - Views_History : \t{ steps} \n\n\
                            - Hierarchy:\t{filepath.read_file(viewObj['jsonpath'])} \n\n \
                            - App_Information:\t{App_Information}\n\n \
                            - the_Target_Area:\t{target}\n\n\
                        ",
                },
               {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64(viewObj['imgpath'])}","detail": "low",},
                    
                },
            ]
        }
    ]
    rsp = ask_gpt4v(messages)
    action = parseObject(rsp)

    filepath.add_log( {"response": rsp, "request":  {
            "role": "user",
            "content": [
                    {
                        "type": "text",
                        "text": prompt_page.get_action
                    },
                {
                        "type": "text",
                        "text": f"\
                            - Views_History : \t{ steps} \n\n\
                            - Hierarchy:\t{(viewObj['jsonpath'])} \n\n \
                            - App_Information:\t{App_Information}\n\n \
                            - the_Target_Area:\t{target}\n\n\
                        ",
                },
               {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{(viewObj['imgpath'])}","detail": "low",},
                    
                },
            ]
        }} )


    action_str = action['Action']
    if(action_str == 'FINISH'): return 'FINISH'
    elif action_str.startswith("tap("):
            # Use regex to extract the element index.
            match = re.search(r"tap\(\s*'([^']+)'\s*\)", action_str)
            if match:
                index_value = match.group(1)
            else:
                index_value = ""
            return {"type": "tap", 'ele':{"index": index_value}}
        
        # Check if the string starts with "text(".
    elif action_str.startswith("text("):
            # Use regex to extract the text content.
            match = re.search(r"text\(\s*'([^']+)'\s*\)", action_str)
            if match:
                msg_value = match.group(1)
            else:
                msg_value = ""
            return {"type": "input",  "msg": msg_value}

    return 



def askFunPath(fun_map):
    messages = [
        {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": prompt_fun.get_path
                    },{
                    "type": "text",
                    "text": f"\
                        - fun_map:{fun_map} \n \
                            \n ",
                    }
            ]}]
    rsp = ask_gpt4v(messages)
    filepath.add_log( {"response": rsp, "request": {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": prompt_fun.get_path
                    },{
                    "type": "text",
                    "text": f"\
                        - fun_map:{fun_map} \n \
                            \n ",
                    }
            ]}})

    functional_logic_paths  =  parseObject(rsp)['functional_logic_paths']
    print(functional_logic_paths)
    for key in functional_logic_paths:
        messages = [{
        "role": "user",
        "content": [
                {
                "type": "text",
                "text": prompt_fun.get_step
                },{
                "type": "text",
                "text": f"\
                    - fun_map:{fun_map} \n \
                    - functional_logic_paths:{key}\n ",
                }
        ]}]
        rsp = ask_gpt4v(messages)
        filepath.add_log( {"response": rsp, "request": {
        "role": "user",
        "content": [
                {
                "type": "text",
                "text": prompt_fun.get_step
                },{
                "type": "text",
                "text": f"\
                    - fun_map:{fun_map} \n \
                    - functional_logic_paths:{key}\n ",
                }
        ]}})
        key['steps'] = parseObject(rsp)['steps']
    fun_map['functional_logic_paths'] = functional_logic_paths
    return fun_map


    


def askFunMap(fun_map,source_page,target_page,actions):

    messages = [
        {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": prompt_fun.get_fun_map
                    },{
                    "type": "text",
                    "text": f"\
                        - actions:{actions}\n\
                        - fun_map:{fun_map} \n \
                            \n ",
                    },{
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64(source_page)}","detail": "low",},
                    }, {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64(target_page)}","detail": "low",},
                    },
            ]}]
    rsp = ask_gpt4v(messages)
    filepath.add_log( {"response": rsp, "request": {
            "role": "user",
            "content": [
                    {
                    "type": "text",
                    "text": prompt_fun.get_fun_map
                    },{
                    "type": "text",
                    "text": f"\
                        - actions:{actions}\n\
                        - fun_map:{fun_map} \n \
                            \n ",
                    },{
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{(source_page)}","detail": "low",},
                    }, {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{(target_page)}","detail": "low",},
                    },
            ]}} )
    return parseObject(rsp)
