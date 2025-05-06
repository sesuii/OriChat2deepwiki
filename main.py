
from utils import filepath
from explore import testModule,initialize_pages

def run():
    while True:
        filepath.initoutput()
        pages,links = filepath.readoutput()
        # 如果页面数据为空，则添加初始页面
        if(len(pages) == 0): 
            initialize_pages(pages)
        filepath.writeoutput(pages,links)
        if all(page.get('isFinished', True) for page in pages):
            print("所有页面测试完毕，退出程序。")
            break

        for  page in pages:
            if page.get('isFinished'):  
                continue
            
            # 寻找待测功能模块
            if all(module.get('isFinished', True) for module in page['functional_modules']):
                # 更新状态后保存
                page["isFinished"] = True  
                filepath.writeoutput(pages,links)
                break
            for module in page['functional_modules']:
                if module.get('isFinished'):  
                    continue

                testModule(pages,links,page['index'],module['index'])
                filepath.writeoutput(pages,links)
                break
            break

run()





