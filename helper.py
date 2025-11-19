import ast
import PIL
import google.generativeai as genai
import pyautogui
from PIL import Image, ImageDraw
import time



width,height = pyautogui.size()
model = genai.GenerativeModel(model_name='gemini-2.5-flash-lite')

def execute_action(action):
    
    if action.startswith("move_to"):
        parts = action.split(" ", 1)
        bbox_str = parts[1]
        bbox = ast.literal_eval(bbox_str)
        
        y = (bbox[0] + bbox[2]) / 2
        x = (bbox[1] + bbox[3]) / 2
        x = (x /1000 ) * width
        y = (y /1000 ) * height
        
        
        pyautogui.moveTo(x, y)
    elif action.startswith("click"):
        pyautogui.click()
    elif action.startswith("type"):
        text = " ".join(action.split()[1:])
        pyautogui.typewrite(text)
    elif action.startswith("enter"):
        pyautogui.press('enter')
    else:
        print(f"Unknown action: {action}")

def screenshot(number):
  image1 = pyautogui.screenshot(f"image{number}.png")
  
def drawMouse():
  screenshot = pyautogui.screenshot()
  mouse_x, mouse_y = pyautogui.position()
  draw = ImageDraw.Draw(screenshot)
  
  cursor_radius = 15
  cursor_color = "red"
  draw.ellipse(
    (mouse_x - cursor_radius, mouse_y - cursor_radius,
     mouse_x + cursor_radius, mouse_y + cursor_radius),
    fill=cursor_color,
    outline=cursor_color
    )
  screenshot.save("image.png")
  
  

def main(command, apiKey):
  genai.configure(api_key=apiKey)
  lastAction = ["start"]
  Continue = True
  counter = 1
  pyautogui.PAUSE = 2.5
 

  base_prompt=('''
  You are the backend controller for a system that operates a user’s computer through step-by-step actions.  
  Users will give natural language requests (e.g. “Open Chrome”, “Search for weather”, “Create a document”). Your job is to output exactly ONE action per response.

AVAILABLE ACTIONS:
1. move_to [ymin, xmin, ymax, xmax]
2. click
3. type text
4. enter

BOUNDING BOX RULES:
- Bounding boxes are ALWAYS in the format: [ymin, xmin, ymax, xmax]
- All values are NORMALIZED between 0 and 1000.
- Example: [100, 200, 250, 350]
- These coordinates refer to the on-screen location of the target in the screenshot.
- When using move_to, you must output ONLY one move_to command and nothing else.
- Never repeat move_to twice in a row. If the previous action was move_to, the next must be click, type, or enter.

ACTION RULES:
- OUTPUT ONLY ONE COMMAND PER TURN.
- DO NOT number commands.
- DO NOT add explanations or extra words.
- Before typing, ALWAYS click the target field first.
- After typing, ALWAYS use enter.
- The cursor appears as a red dot on the screenshot: use it to understand current position.
- Ensure each move_to shifts the cursor closer to the target.
- If clicking does nothing, slightly move first then click again.
- When the entire task is completed, output exactly: Done

CONSTRAINTS:
- No extra punctuation, no newlines, no multiple commands.
- Follow the sequence: click → type → enter where appropriate.

               
               
               ''')

  

  instruction = command
  time.sleep(2)
  while Continue == True: 
    drawMouse()
    image_path ="./image.png"
    file = PIL.Image.open(image_path)
    
    prompt = (
            f"{base_prompt}\n"
            f"Task: {instruction}\n"
            f"Previous actions : {", ".join(lastAction)}\n"
            f"Action number: {counter}\n"
        )
    
    response = model.generate_content([prompt,file])
    action = response.text.strip().split('\n')[0]
    print(action)
    
    if action.startswith("Done"):
      Continue = False
    execute_action(action)
    lastAction.append(str(counter) +"." + action)
    counter = counter + 1
    print(counter)
    

if __name__ == "__main__":
    main()
  