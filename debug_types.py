
import google.genai.types as types
print("Available types in google.genai.types:")
for x in dir(types):
    if "Video" in x:
        print(f" - {x}")
