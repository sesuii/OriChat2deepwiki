from utils import filepath,mark_image,gpt
import json,shutil,re

pages,links = filepath.readoutput()
n = len(pages)
matrix = [[[] for _ in range(n)] for _ in range(n)]
for idx,page in enumerate(pages):
    shutil.copy(page['page_config']['imgpath'], './img')


for idx, link in enumerate(links):
    for idxstep, step in enumerate(link):
        if(step['to'] == 'outofApp'):
            pass
        else:
            obj =  {'type':step['type'],
                    **step['ele'],
                    'assets':step['assets']
                    }

            if all(obj != act for act in matrix[step['from']][step['to']]):
                matrix[step['from']][step['to']].append(obj)
            if(not matrix[step['from']][step['to']]):
                 matrix[step['from']][step['to']].append(obj)
arr= []
infos = []

def getlink(rowindex):
    row = matrix[rowindex]
    start_img = pages[rowindex]['page_config']['imgpath']
    boxes = []
    end_ids = []
    imgs = []
    infos.append({
            "pageId":rowindex,
            "page_overview":pages[rowindex]['page_overview'],
        })
    for j, cells in enumerate(row):
        infos.append({
            "pageId":j,
            "page_overview":pages[j]['page_overview'],
        })
        for cell in cells:
            result_str= []
            for k, v in cell.items():
                if k  in ('text', 'class', 'resource-id','content-desc'):
                    result_str.append(f"{v}")
            nums_str = re.findall(r"\d+", cell['bounds'])
            boxes.append(list(map(int, nums_str)))
            end_ids.append(str(j))
            arr.append({
                'source_page_id':str(rowindex),
                'target_page_id':str(j),
                'action_id':len(arr),
                'type':cell['type'],
                'content':' '.join(result_str)
                })

            imgs.append(cell['assets']['imgpath'])
    print(end_ids)
    if end_ids:
        mark_image.draw_boxes_with_labels(
            image_path=start_img,
            boxes=boxes,
            ids = end_ids,
            output_path="example_marked.jpg",
            source_page_id = rowindex
        )
        mark_image.concat_images_horizontally(
            image_paths = imgs,
            ids = end_ids,
            output_path="concat_horizontal.jpg"
        )
    

    


if __name__ == "__main__":
    # fun_log_map  = {}
    # for idx, link in enumerate(pages):
    #     getlink(idx)
    #     for key in arr:
    #         print(key)
    #         print('\n')
    #     fun_log_map = gpt.askFunMap(fun_log_map,'example_marked.jpg',"concat_horizontal.jpg",arr)
    #     print(fun_log_map)
    # filepath.write_json('logic.json',fun_log_map)
        res = gpt.askFunPath(filepath.read_json('logic.json'))
        filepath.write_json('stepdesc.json',res)
    
        
    
    

