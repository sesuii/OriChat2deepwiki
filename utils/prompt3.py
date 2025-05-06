update_view   = '''
I will provide you with 2 page screenshots, its corresponding XML layout files, and a description of the **old functional modules** present in the previous version of the application.

Please perform the following:

1. **Page Information**: You will receive:
   - Old version and new version page screenshots.
   - Old version and new version XML layout files.
   - Description of **old functional modules** (simple description, such as "Login Module", along with **bounds** and **index** for each module).

2. **Task**: Based on the provided inputs, please perform the following:
   - **Identify new functional modules**: Analyze the differences between the old and new versions based on the screenshots and XML files. Identify whether any functional modules have changed (added, removed, or modified).
   - Based on the old functional module descriptions, check whether any new UI components have appeared that introduce new interactive functionalities.Ensure that detected new modules contain interactive elements (e.g., buttons, input fields, menus).

3. **Output Format**:
Return the results in the following JSON format:

{
  "new_or_modified_modules": [
    {
      "module_name": "Memo Module",
      "bounds": "[0, 0][100, 50]",
      "index": "0-1",
      "interactive_elements": ["0-1-0", "0-1-2"],
      "test_plan": {
        "type": "Random Click",
        "steps": [
          "Click on the 'Add Item' button",
          "Verify that a new item is added to the list."
        ]
      }
    }
  ]
}
'''
