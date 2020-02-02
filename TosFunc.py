import re

def removestuff(s):
    return re.sub("\{.*?\}","",s.replace("{nl}","\n"))
def ns(v):
    return ("%2g" % v).strip()