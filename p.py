
import re
txt = "Aa12345aA"
pattern = r"[0-9a-zA-Z]{5}" 

print (re.search(pattern , txt) )

