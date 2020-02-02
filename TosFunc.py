import re

def removestuff(s):
    return re.sub("\{.*?\}","",s.replace("{nl}","\n"))
