import os

file = "/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/ultralytics"
absolute = os.path.abspath(file)
folder = os.path.dirname(absolute)

new_path = "/Users/guoyueyao/Desktop/supervisor/supervisor/model"

new = os.path.join(new_path,os.path.basename(absolute))
print("road:", new)

