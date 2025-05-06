get_fun_map = '''
用户提示：

你是一个熟悉UI页面功能识别与功能逻辑图构建的智能助手。接下来你将结合给定的移动端App页面截图与相关描述信息，严格按照以下步骤构建完整、精确的功能逻辑图（包含独立孤立功能点，如页面内可独立使用、无后续跳转的功能）：

你会收到的信息包括：
1. **页面截图**：明确以 "{action_id}-p{target_page_id}" 的方式红框标注了当前页面可交互控件对应的操作动作与目标页面。
2. **所有目标页面截图拼接页**：屏幕截图经过拼接，每张截图下方有清晰的操作序号 和 页面id  (action_id target_page_id)。
3. **操作信息列表**：每个操作记录来源页面id、目标页面id、action_id、动作类型和具体控件文本。
4. **当前已有功能逻辑图**：已有功能逻辑图记录已有功能节点和它们之间的业务流转关系。
5. **相关页面功能描述**：简要描述页面功能，可能包含无页面跳转、单独出现即可完成业务逻辑的功能（比如搜索、刷新页面、切换显示模式等）。

请按照以下步骤严格执行任务：

【步骤一：识别功能节点（包含孤立功能节点）】
- 根据提供的页面功能描述、页面截图以及操作信息：
    - 提取页面内的业务功能（尤其是不产生页面跳转、独立完成的单一业务功能，例如搜索、下拉刷新等），并生成相应的功能节点描述。
    - 功能合并，如果某些操作的操作效果、跳转页面及功能执行路径都一致，则在功能逻辑图上建议合并。
    - 如果某个目标页面ID在已有功能逻辑图中不存在，需基于页面描述生成新的功能节点，并使用截图标注的 page_id 来标志它（例如 "page_id": 3）。确保每个功能节点均包含明确的功能描述。

【步骤二：映射页面流转关系】
- 根据页面截图中红框标注的信息 "{action_id}-p{target_page_id}"，严格校验并映射对应的来源页面和目标页面之间的跳转关系。
- 如果发现页面跳转操作对应的页面ID重复或功能点重叠，请合并处理避免冗余节点。

【步骤三：更新功能逻辑图】
- 将新识别的功能节点（包括孤立功能节点）和页面关系整合进已存在的功能逻辑图。
- page_id 和 action_id 必须严格与页面截图内给定的ID 完全一致。
- 确保所有功能节点及页面关系均已准确体现于最终输出的功能逻辑图内，无遗漏、无冗余。

【输出要求】：
- 输出严格遵循以下JSON格式，请勿包含多余的解释说明或备注，并准确引用截图标注的所有 page_id：

{
    "function_nodes": [
        {
            "function_id": "功能节点ID，从0开始顺序增长",
            "function_name": "功能名称或清晰的业务逻辑描述",
            "related_pages": [
                {
                    "page_id": "严格采用截图标注的信息，比如'1'，不可擅自修改或遗漏",
                    "page_name": "清楚明确的页面名称或描述"
                }
            ]
        }
    ],
    "logic_relations": [
        {
            "source_function_id": "源功能节点ID",
            "target_function_id": "目标功能节点ID",
            "description": "描述两个功能节点之间的业务逻辑流转或交互场景",
            "operation_description": "点击【商品选购】按钮"
        }
    ]
}

【注意事项】：
- 必须明确识别和表达页面内部无跳转独立功能节点，不要遗漏。
- 必须严格且准确使用截图标注的 "{action_id}-p{target_page_id}" 信息进行页面id的验证校准，不允许额外创造ID或遗漏已有ID。
- 输出中不可出现任何与截图标注不符的page_id或action_id信息。

现在请根据上述规则完成任务。
'''


temp = '''


任务背景：
现在你需要基于已经抽取好的业务功能逻辑图，对其中各个功能结点形成有效的完整功能逻辑路径，以满足后续精准测试序列生成和功能缺陷检测。

任务目标：
针对给定的功能逻辑图，我们需要自动地、智能地提取出满足如下标准的功能逻辑路径集合：

每条路径都是真实且具有实际意义的业务操作流。
每条路径都必须具备明确的业务起点（例如：首页进入、功能模块入口）以及明确的业务终点（例如提交、返回、查看结果、保存、付款完成等明确的出口功能）。
路径中的每一步都明确对应到实际可操作的UI交互和页面状态变化, 能够实际执行并触发具体的UI状态转移与交互效果。
每条路径需清晰体现完整的功能逻辑，确保不会遗漏关键中间步骤或核心功能节点。
具体执行步骤与约束条件：
STEP1：识别与定义路径的逻辑起点和终点。

路径起点必须为业务逻辑图的功能入口节点（主页面或某功能起始节点）。
路径终点必须为具有明确业务含义的功能出口节点（如功能任务完成、确认提交、返回到起始页面、支付成功、保存信息等明确标识的功能性页面）。
STEP2：分析并确定功能节点之间的关联关系。

根据节点之间的功能交互关联关系定义一条有效路径。
每个路径节点应当根据功能逻辑要求逐步推进，不应当出现逻辑断层或不相关功能跳跃。

STEP3：路径约束条件及规则定义。
路径提取必须遵循以下约束规则：
a. 路径完整性约束：
所生成的每条逻辑路径必须确保能够表示从起始业务功能节点到最后具有现实意义的功能终点之间的完整有效操作流程，不允许出现不完整或非业务价值路径。

b. 状态转移有效性约束：
每步路径转移必须对应于实际的UI界面和具体的可执行操作，不允许设计理论上存在而实际UI实现不存在的不真实路径。

c. 逻辑合理性约束：
所提取路径的每个功能转移必须符合基本的业务逻辑和实际使用场景。不应出现明显不合理或无法实际完成的功能跳转步骤。

输出结果：

输出具有明确起止节点定义及具体路径步骤的功能逻辑路径序列集合。
每条路径以可计算机执行的结构化形式输出，包含路径的起止点、功能操作步骤序列、涉及UI动作与元素交互描述，以及清晰对应的功能节点标识。
下面给出一个明确格式的输出示例，以确保大模型生成的路径序列能够便于工具自动解析使用：

输出示例：
{
    "functional_logic_paths": [
        {
            "path_id": 0,
            "start_function_id": 0,
            "end_function_id": 2,
            "path_description": "从首页进入商品页面并选择商品提交订单",
            "expected_result": "显示提交订单成功的相关信息和提示",
             "steps": [
                {
                    "step_id": 0,
                    "function_id": 0,
                    "function_name": "首页",
                    "operation_description": "点击【商品选购】按钮"
                },
                {
                    "step_id": 1,
                    "function_id": 1,
                    "function_name": "商品选择页",
                    "operation_description": "选择商品后点击【确认提交订单】按钮"
                },
                {
                    "step_id": 2,
                    "function_id": 2,
                    "function_name": "订单提交确认页面",
                    "operation_description": "页面加载后展示订单提交确认信息"
                }
            ],
        }
    ]
}


'''

get_path = '''
你现在作为一个自动生成UI测试业务逻辑路径的智能助手，我将给你提供一张完整的功能逻辑图，以及序列化呈现的功能节点信息。

你需要完成以下任务：

根据所提供的功能逻辑图，以JSON形式列举出每一条从起始点到终点，真实存在且具有实际业务意义的业务操作路径信息。

每条路径都必须满足：

路径起点和终点应代表实际用户业务场景明确的开始与结束，以真实业务逻辑为依据进行确定。
路径整体顺序应严格按照实际业务逻辑中各功能步骤的执行顺序进行排序。例如具有先后依赖关系的功能节点，需要明确将前置功能排在依赖该功能之前（如新增功能应该排在排序和搜索之前）。
路径的功能描述需简洁准确描述实际的业务流程细节，不要抽象、不明确。
"expected_result" 字段用于描述路径终点的预期目标或预期结果，用精准易懂的语言阐述用户完成此项任务后在UI上的反馈状态和呈现内容。
请按照以下JSON示例格式，明确提供每条路径信息：

{
    "functional_logic_paths": [
        {
            "path_id": 0,
            "start_function_id": 0,
            "end_function_id": 2,
            "path_description": "从首页进入商品页面并选择商品提交订单",
            "expected_result": "显示提交订单成功的相关信息和提示",
            
        }
    ]
}


'''

get_step = '''
你现在作为一个自动生成UI测试业务逻辑路径的智能助手，我将提供一张完整的业务逻辑图，以及序列化呈现的功能节点信息。
请你基于之前识别并提取出的路径起终点信息，严格遵循以下的逻辑与约束条件，返回具体的功能流程节点步骤：
以下几点是你必须严格遵守的逻辑和约束条件：

a. 路径完整性约束
你设计出的每条功能业务逻辑路径必须从步骤一给定的业务起始功能节点（start_function_id）开始，到业务终点功能节点（end_function_id）结束。路径中间不能遗漏关键步骤，所有必经功能节点必须完整表述。

b. 状态转移有效性约束
路径中的每次功能节点转移必须明确对应实际UI界面的真实可执行操作，不能有虚构或UI未实现的跳转路径。

c. 逻辑合理性约束
每个节点的功能操作过程必须符合实际业务逻辑和用户使用习惯，前后节点必须形成合理且连续的、符合业务逻辑的操作序列，不允许出现不符合实际情况或跳跃过远，导致用户无法连续执行的操作步骤。

请按照以下JSON示例格式，逐条梳理并生成步骤一中每条功能路径的详细功能节点信息，并清晰提供每个节点所需执行的具体操作。
{
     "steps": [
                {
                    "step_id": 0,
                    "function_id": 0,
                    "function_name": "首页",
                    "operation_description": "点击【商品选购】按钮"
                },
                {
                    "step_id": 1,
                    "function_id": 1,
                    "function_name": "商品选择页",
                    "operation_description": "选择商品后点击【确认提交订单】按钮"
                },
                {
                    "step_id": 2,
                    "function_id": 2,
                    "function_name": "订单提交确认页面",
                    "operation_description": "页面加载后展示订单提交确认信息"
                }
            ],
}


'''


get_act = '''

You are an expert assistant for mobile UI automated testing. Your goal is to ensure accurate, reliable, and highly efficient automated UI test execution.

Below is the detailed information needed for your current task:

Functional Logic Path:
{Clearly describe the functional logic path or test scenario that must be precisely implemented}

Current Screen State:
{Screenshot image of the current screen}

XML element details:
{XML file containing detailed information of all UI elements available on the current screen}

Previous Interaction History:
{List of actions previously executed, including the system responses, for context reference}

Your Task:

Analyze carefully both the provided screen screenshot and the detailed XML element structure information.
Strictly follow and precisely execute interaction steps based on the defined functional logic path provided.
Clearly suggest the next interaction step required (e.g., tap an element, provide input text), adhering strictly to the logical path guidance and current UI state.
If and only if the targeted functionality corresponding to the provided functional logic path is completely achieved (there is no further step needed), clearly output "FINISH".
Important notes:

You have access to the following callable functions to automate interactions accurately on the mobile UI:

A. tap(element: str)
Taps a specified UI element on the screen. "element" parameter refers strictly to the 'index' attribute value from the provided XML file. For instance, calling tap('0-1') triggers the UI element whose 'index' attribute is '0-1'. You must ensure the element described actually exists in the provided XML.

B. text(text_input: str)
Inputs text into a currently focused input box. This function must only be invoked if an on-screen keyboard is visible. The input text string must be enclosed within double quotation marks. For example, calling text("Hello, world!") types "Hello, world!" into the currently focused text input field.

Please respond strictly according to the structured JSON output format below:

{
  "Thought": "Briefly describe your reasoning about the current UI state, the logic path progress, and justify clearly why a particular interaction must be executed next.",
  "Action": "tap('element-index')" // or "text(\"input text\")" // or "FINISH" (Only use FINISH if the full scenario defined by the functional logic path is completed. Always provide a valid callable function or FINISH, do not provide anything else in this field.),
  "Summary": "Briefly describe the expected result or consequence after executing the suggested action step in relation to the test path scenario provided."
}
Example Response:

{
  "Thought": "Login credentials have been successfully entered, and the 'LOGIN' button is now clearly visible and enabled. Clicking this button is the next required step to complete the login process and proceed to the home screen according to the provided logic path.",
  "Action": "tap('0-1-7')",
  "Summary": "User taps the 'LOGIN' button. The application should validate login credentials and navigate successfully to the home screen."
}

'''