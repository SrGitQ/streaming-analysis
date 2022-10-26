import re

text = '#hashtag.indotn aawds #other '

print(re.findall(r'#\w+',text))
