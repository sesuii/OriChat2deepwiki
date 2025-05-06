get_functional_modules = '''

I will provide you with a page screenshot and its corresponding XML layout file. Based on these inputs, please perform the following analysis and return structured output:

 **Page Functionality Module Recognition and Interactive Element Identification**:
   - Identify **all functional modules** on the page based on the screenshot and XML layout.**Prioritize** them based on user usage habits.Do not omit any module or interactive element.
   - For each **functional module**, identify **all interactive elements**.
   - For each **functional module**, provide a **UI Test Plan** that includes:
     - **a.Bounds**: The `bounds` attribute from the XML file, which gives the coordinates and size of the functional module.
     - **b.Index**: The `index` attribute, which represents the position of the module in the layout hierarchy.
     - **c.Test Plan Type**:
          c-1. **Random Click**: should be used for elements that are functionally similar, where only one needs to be tested at a time.
          c-2. **Sequential Click**:for elements with different functions, where each element needs to be tested sequentially for its unique functionality.
          c-3. **Other**: reserved for more complex scenarios, like form filling, that require detailed, step-by-step testing.
     - **d.The interactive elements** for each functional module should be listed by their **index** only, without needing to list other properties (e.g., resource-id, content-desc, etc.).    



Return the results in the following structured JSON format:
{
    "page_overview": "This login page is designed to authenticate users by allowing them to enter their credentials. It features distinct input fields for the username and password, a prominent login button to submit the credentials, and a 'Forgot Password' link to assist users in recovering their account access. These interactive elements are integral to the authentication process, ensuring that users can securely log in and access their personalized dashboard.",
    "functional_modules": [
        {
            "module_name": "Login Module",
            "bounds": "[0, 0][100, 50]",
            "index": "0-1",
            "interactive_elements": [#Important**: For the **interactive_elements** field, ensure that you only include the index values that exist in the provided **XML layout file**. These indices are the crucial basis for identifying the interactive elements.
                "0-1-0",
                "0-1-2"
            ],
            "test_plan": {
                "type": "Random Click",
                "steps": [
                    "Click on the login button",
                    "Verify that the login action is triggered"
                ]
            }
        }
    ]
}



'''

get_representative_ui_elements='''
I will provide you with a page screenshot and its corresponding XML layout file. Based on these inputs, please perform the following analysis and return structured output:

 - **Comprehensive Elements for Repeat Page Detection** 
      - Based on the UI screenshot and XML layout, identify all representative UI elements that remain stable across different sessions and are capable of distinguishing one page from another or identifying the same page when revisited.
      - Classify these elements into three categories:
          Title: Typically a static, prominent text or label that indicates the page’s primary purpose (e.g., “Login,” “Product Details”).
          Primary_Action_Button: A key interactive element, such as “Submit,” “Next,” or “Buy,” which plays a critical role in user flow.
          Fixed_Layout_Components: Commonly stable layout elements like a navigation bar, tool bar, or fixed banner.
      - Include as many elements as possible that may provide stable identifying properties. If truly no element qualifies for a category, you may omit that category. However, borderline cases or partially suitable elements should still be included if they offer potential value for repeat page detection.
      - Instead of other identifiers, use the XML index attribute to uniquely specify each element in the output.


Please carefully select only attributes that are stable, representative, static, and available directly on the element itself according to the XML data provided. There is no need to list all given attributes; include only those you deem genuinely representative and stable.
Return the results in the following structured JSON format:
    {
    "representative_ui_elements": {
        "Title": [
            "0-1",
            "0-2",
            "0-3"
        ],
        "Primary_Action_Button": [],
        "Fixed_Layout_Components": []
    }
    }

'''


get_action = '''
I will provide you with a page screenshot, its corresponding XML layout file, historical operation records, and a simple description of a specific functional module to test.

Please perform the following:

1. **Page Information**: You will receive:
   - Page screenshot (used to identify the structure of the page and the elements).
   - XML file (provides layout information, element properties, hierarchy, etc.).
   - Historical operation records (previous steps).
   - Specific functional module description (simple description, such as "Login Module", along with **bounds** and **index**).

2. **Task**: Based on the provided inputs, generate one test step for the **specific functional module** described, You can call the following functions to interact with elements to control the smartphone:
    A. tap(element: str)
    This function is used to tap an UI element shown on the smartphone screen."element" is the 'index' attribute value of the element based on XML file. It is important to ensure that the element specified actually exists within the specific functional module. A simple use case can be tap('0-1'), which taps the UI element with the 'index' attribute value '0-1'.
    B. text(text_input: str)
    This function is used to insert text input in an input field/box. text_input is the string you want to insert and must be wrapped with double quotation marks. A simple use case can be text("Hello, world!"), which inserts the string "Hello, world!" into the input area on the smartphone screen. This function is only callable when you see a keyboard showing in the lower half of the screen.

3. **Important**:  To ensure that all elements are explored efficiently, given the constraints of performing no more than 10 actions. Maintains the action limit by focusing on essential interactions that provide the most information about the UI’s behavior.

4. **Output Format**:
Return the result in the following JSON format:

```json
{
  "Thought": "The user needs to complete a complex action within the login module, such as filling out a form or interacting with multiple elements.",
  "Action": "tap('0-1-0')",  // Or "text('test input')" // or "FINISH" #If you ensure the exploration of the **specific functional module**  is completed, you should output FINISH. You cannot output anything else except a function call or FINISH in this field.
  "Summary": "User taps on the 'Login' button. The system should respond by processing the login request and redirecting the user to the homepage."
}
'''
