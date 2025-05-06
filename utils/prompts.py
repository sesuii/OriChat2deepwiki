get_desc = '''
In this UI functionality testing task, you'll receive:
- A screentshot.
- A view hierarchy file.
- App Information.

Task Overview:
- Based on the provided information, you should divides the UI into distinct areas with the understanding that different areas typically do not overlap, ensuring a clear and organized partitioning. Detailing the observations, documentation, contained elements, testing thoughts, and explanations for each area with specific functions or purposes. such as a Bottom navigation bar,a form requires a sequence of actions to test, or a list.
- treats the entire form as a single area, grouping all the elements together and outlining the collective observations and testing plan.
- Understanding functional partitioning of the UI interface involves the following aspects:
    Area Division: The UI interface is divided into different areas, with each area typically associated with specific functions, tasks, or information. For example, the main screen of an application may include a top navigation bar, a content area, and a bottom navigation bar, each serving different purposes.
    Function Categorization: Within each area, related functions or operations are usually grouped together. For example, a settings menu may include various options related to application settings, while a message list area may contain functions related to message management.
    User Guidance: Functional partitioning helps users navigate and use the application more easily. Users can directly go to the respective area based on the desired function, without having to browse through the entire interface.
    Consistency: Functional partitioning helps ensure the consistency of the UI interface, making the application look neater and more understandable. Each area can follow consistent design and interaction patterns to provide a better user experience.

Return the results only in Standard JSON format with the following structure: 
[{
    "Bounds":..., # "bounds" attribute value of the element for this area from view hierarchy file. The bounds are given in the format \"[left,top][right,bottom]\" as per the Android view hierarchy convention.
    "Observation": ...  # Describe what you observe in this region,
    "Documentation": ...  # Describe the functions of the region,
    "Elements": Lists all elements without omitting in the area, list only the index field from the view hierarchy file such as ["0-0-0-0-1","0-0-0-0-2","0-0-0-0-3"],No index field beyond those present in the view hierarchy file are included in the returned content.
    "Container":... # the index field of the element means the region,
    "Thought": Outlines the planned approach for testing,You cannot output anything else except "click_each" or "click_select" or "others".
        Criteria for click_each:
            Each elements performs a unique function that needs to be tested individually. 
        Criteria for click_select:
            The elements perform similar functions (such as filtering products by category, we will select representative elements from similar groups instead of testing every item individually.Maintains the action limit by focusing on essential interactions that provide the most information about the UI’s behavior.
        others Implies a sequence of actions will be performed such as filling a form,or other types of actions will be performed such as input_text or swipe, to test the workflow or interaction order among the elements.
    "Explain":Explain why you chose "click_each" or "click_select" or "others",
},{
    "Bounds":...,
    "Observation": ...  ,
    "Documentation": ...  ,
    "Container": ... ,
    "Elements": ...,
    "Thought":...
}]
'''

get_action = '''
Background Context:
The task is to perform actions in a Target_Area of the UI that links to distinct views. To ensure that all elements are explored efficiently, given the constraints of performing no more than 10 actions. Maintains the action limit by focusing on essential interactions that provide the most information about the UI’s behavior.
you need to avoid redundant actions based on Action History.

In this UI functionality testing task, you'll receive:
- Action History,
- A screentshot.
- A view hierarchy file.
- App Information.
- the Target Area in the page,
- Page Segmentation in the page with the following structure,Do not add comments in JSON format data: 
[{
    "Bounds":..., # 'bounds' attribute value of the element for this area from view hierarchy file. The bounds are given in the format \"[left,top][right,bottom]\" as per the Android view hierarchy convention.
    "Observation": ...  # Describe what you observe in this region,
    "Documentation": ...  # Describe the functions of the region,
    "Elements": Lists all elements without omitting in the area, list only the index field from the view hierarchy file such as ['0-0-0-0-1','0-0-0-0-2','0-0-0-0-3'],No count values beyond those present in the view hierarchy file are included in the returned content.
    "Container":... # the index field of the element that is the container of the region,
    "Thought": Outlines the planned approach for testing,You cannot output anything else except 'click_each' or 'click_select' or 'others'.
    "Explain":Explain why you chose 'click_each' or 'click_select' or 'others',
}]

You can call the following functions to interact with elements to control the smartphone:

1. tap(element: str)
This function is used to tap an UI element shown on the smartphone screen.
"element" is the 'index' attribute value of the element based on Current_Page_hierarchy. It is important to ensure that the element specified actually exists within the current view hierarchy.
A simple use case can be tap('0-1'), which taps the UI element with the 'index' attribute value '0-1'.

2. text(text_input: str)
This function is used to insert text input in an input field/box. text_input is the string you want to insert and must 
be wrapped with double quotation marks. A simple use case can be text("Hello, world!"), which inserts the string 
"Hello, world!" into the input area on the smartphone screen. This function is only callable when you see a keyboard 
showing in the lower half of the screen.

3. long_press(element: str)
This function is used to long press an UI element shown on the smartphone screen.
"element" is the 'index' attribute value of the element based on Current_Page_hierarchy. It is important to ensure that the element specified actually exists within the current view hierarchy.
A simple use case can be long_press('0-1'), which long presses the UI element with the 'index' attribute value '0-1'.

4. swipe(element: str, direction: str, dist: str)
This function is used to swipe an UI element shown on the smartphone screen, usually a scroll view or a slide bar.
"element" is the 'index' attribute value of the element based on Current_Page_hierarchy. It is important to ensure that the element specified actually exists within the current view hierarchy.
"direction" is a string that represents one of the four directions: up, down, left, right. "direction" must be wrapped with double quotation 
marks. "dist" determines the distance of the swipe and can be one of the three options: short, medium, long. You should 
choose the appropriate distance option according to your need.
A simple use case can be swipe('0-1', "up", "medium"), which swipes up the UI element with the 'index' attribute value '0-1' for a medium distance.

Return the results in JSON format with the following structure: 
{
"Thought": # To complete the exploration from Target_Area, what you plan to do.
"Action": # The function call with the correct parameters to complete the exploration. If you ensure the exploration of Target_Area is completed, you should output FINISH. You cannot output anything else except a function call or FINISH in this field.
"Summary": # Summarize this action.
}

'''

get_visualmap = '''
Background Summary:
You are an agent that is trained to analyze an application and update its visual map. Some actions have been taken that lead app from Initial_Page to Current_Page.

In this UI functionality testing task, you'll receive:
- Old_Version_VisualMap,
- Your_Past_Actions,
- App_Information,
- Current_Page_hierarchy,
- Current_Page_screentshot as the second picture,

Return the results in Standard JSON format with the following structure: 
[{
    
    "isRecorded": <Verify if the Old_Version_VisualMap includes Current_Page, if true, return the pageId. You cannot output anything else except pageId or "false">,
    "Pagetransition":<Verify if there is a page transition, indicating that the user has entered a new functionality of page or view. You cannot output anything else except "true" or "false">,
    "Documentation:<describe the function of the element in Your_Past_Actions>
}]


'''

ask_role_of_page = '''
 the task is comparing two image to determine if they represent different states of the same page.
 the factors to consider is their roles in the business or functional logic.
Return the results in Standard JSON format with the following structure: 
{
    "Judgment": <You cannot output anything else except "true" or "false">,
    "Reason":<...>,
    "Logic": <such as These two pages perform the same function within the application, such as displaying similar content or executing similar actions, so they are considered different states of the same page in terms of business logic.>

}
'''
