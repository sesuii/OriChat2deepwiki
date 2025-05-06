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

3. **Important**: Please ensure that your test steps only involve the specific functional module I have provided and do not consider other unrelated modules on the page. To ensure that all elements are explored efficiently, given the constraints of performing no more than 10 actions. Maintains the action limit by focusing on essential interactions that provide the most information about the UI’s behavior.

4. **Output Format**:
Return the result in the following JSON format:

```json
{
  "Thought": "The user needs to complete a complex action within the login module, such as filling out a form or interacting with multiple elements.",
  "Action": "tap(element: '0-1-0')",  // Or "text('test input')" // or "FINISH" #If you ensure the exploration of the **specific functional module**  is completed, you should output FINISH. You cannot output anything else except a function call or FINISH in this field.
  "Summary": "User taps on the 'Login' button. The system should respond by processing the login request and redirecting the user to the homepage."
}
'''