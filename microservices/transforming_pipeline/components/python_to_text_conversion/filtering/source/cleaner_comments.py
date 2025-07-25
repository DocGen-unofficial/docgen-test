import pandas as pd
import re

def remove_comments_and_docstrings(code: str) -> str:
    code = re.sub(r'("""|\'\'\')(?:.|\n)*?\1', '', code)
    code = re.sub(r'#.*', '', code)
    return code 
    
def cleaner(content: list) -> list:
    content = content.apply(remove_comments_and_docstrings)
    return content
