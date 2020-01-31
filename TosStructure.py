from DicConverter import DicConverter
import pandas
import re
class JobTree:
    jobs=[]

class Job:
    classname=""
    clsid=0
    name=""
    classmaster=""
    engname=""
    lores=""
    description=""
    skills=[]
    attributes=[]
    ishidden=False
    STR=0
    CON=0
    INT=0
    SPR=0
    DEX=0
    jobtype=0
    fullcompatibilityclasses=""
    partialcompatibilityclasses=""
    similarclasses=""
    specialeffectclasses=""
    trivia=""
    costumeandoutfits=""

class Skill:
    description=""
    caption2=""
    classname=""
    clsid=0
    name=""
    maxlv=None
    unlocklv=0
    attributes=[]
class Attribute:
    name=""
    clsid=0
    classname=""
    description=""
    addspend=""
    reqlv=None
    maxlv=0
    arts=False


def generateAttribute(conv:DicConverter,job:Job,attrdata:Attribute):
    attr=Attribute()
    if(not job.engname in conv.skilltable.abilityjob):
        return attr;
    jobattrdata=conv.skilltable.abilityjob[job.engname]

    attr.clsid=attrdata["ClassID"]
    attr.classname=attrdata["ClassName"]
    byclassname=jobattrdata[jobattrdata["ClassName"]==attr.classname]
    attr.description=conv.dictable.krtojp(attrdata["Desc"])
    attr.addspend = conv.dictable.krtojp(attrdata["AddSpend"])
    attr.name=conv.dictable.krtojp(attrdata["Name"])
    attr.reqlv=byclassname["UnlockArgNum"]
    attr.maxlv =byclassname["MaxLevel"]

    if(len(byclassname)>0 and "HIDDENABIL" in byclassname["ScrCalcPrice"].iloc[0]):
        attr.arts=True
    return attr
def generateSkills(conv:DicConverter,job:Job,skillname:str):
    skill=conv.skilltable.skill[conv.skilltable.skill["ClassName"]==skillname]
    skilltree = conv.skilltable.skill[conv.skilltable.skilltree["SkillName"] == skillname]
    skill.description=skill[conv.dictable.krtojp(skill["Caption"])]
    skill.caption2 = skill[conv.dictable.krtojp(skill["Caption2"])]
    skill.classname=skill["ClassName"]
    skill.clsid=skill["ClassID"]
    skill.maxlv=conv.skilltable.skilltree["MaxLevel"]
    skill.reqlv=conv.skilltable.skilltree["UnlockClassLevel"]
    for attr in conv.skilltable.ability.iterrows():
        if(attr[1]["SkillCategory"]==skillname):
            skill.attributes.append(generateAttribute(conv,job,attr[1]))
    return skill
def removebrace(arg):
    return re.sub("\{.*?\}","",arg,)
def findMasterName(conv,jobjpname):
    for k,v in  conv.dictable.dicidtojp:
        m=re.search("")
def generateJob(conv: DicConverter, jobdata:Job):
    job=Job()
    job.clsid = jobdata["ClassID"]
    job.classname = jobdata["ClassName"]
    job.name = conv.dictable.krtojp(jobdata["Name"])
    job.engname = jobdata["EngName"]
    job.STR = jobdata["STR"]
    job.CON = jobdata["CON"]
    job.INT = jobdata["INT"]
    job.SPR = jobdata["MNA"]
    job.DEX = jobdata["DEX"]

    desc=conv.dictable.krtojp(jobdata["Caption1"])
    m = re.search("(.*)\{nl\}(.*?)$", desc)
    if(m is not None):

        job.description=removebrace(m.group(2))
        job.lores=removebrace(m.group(1))
    else:
        job.description=removebrace(desc)
        job.lores=""
    print(job.description+".."+job.lores)
    # job attributes
    for attr in conv.skilltable.ability.iterrows():
        if(attr[1]["SkillCategory"]=="All"):
            job.attributes.append(generateAttribute(conv,job,attr[1]))
    # skills
    for skillintree in conv.skilltable.skilltree[conv.skilltable.skilltree["ClassName"]==job.classname].iterrows():
        job.skills.append(generateSkills(conv,job[1],skillintree["SkillName"]))
    return job
def generateJobTree(conv:DicConverter):
    tree=JobTree()
    for j in conv.skilltable.job.iterrows():
        print(j[1]["EngName"])
        tree.jobs.append(generateJob(conv,j[1]))
    return tree