from DicConverter import DicConverter
import pandas
import re

ctrltype={
    "Warrior":4,
    "Scout":3,
    "Wizard":5,
    "Cleric":2,
    "Archer":1,
}

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
    rank=0
    fullcompatibilityclasses=""
    partialcompatibilityclasses=""
    similarclasses=""
    specialeffectclasses=""
    trivia=""
    costumeandoutfits=""
    ctrltype=""
class Skill:
    description=""
    caption2=""
    classname=""
    clsid=0
    name=""
    maxlv=None
    reqlv=0
    iconname=""
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
    iconname=""

def generateAttribute(conv:DicConverter,job:Job,attrdata:Attribute):
    attr=Attribute()
    if(not job.engname in conv.skilltable.abilityjob):
        return None
    jobattrdata=conv.skilltable.abilityjob[job.engname]

    attr.clsid=attrdata["ClassID"]
    attr.classname=attrdata["ClassName"]
    byclassname=jobattrdata[jobattrdata["ClassName"]==attr.classname]
    if(len(byclassname)==0):
        return None
    attr.description=re.sub("\*","\n",conv.dictable.krtojp(attrdata["Desc"])).strip()
    attr.addspend = conv.dictable.krtojp(attrdata["AddSpend"])
    attr.name=conv.dictable.krtojp(attrdata["Name"])
    attr.reqlv=byclassname["UnlockArgNum"].item()
    attr.maxlv =byclassname["MaxLevel"].item()
    attr.iconname=attrdata["Icon"]
    if(len(byclassname)>0 and "HIDDENABIL" in byclassname["ScrCalcPrice"].iloc[0]):
        attr.arts=True
    return attr
def generateSkills(conv:DicConverter,job:Job,skillname:str):

    pa=conv.skilltable.skill[conv.skilltable.skill["ClassName"]==skillname]
    pt=conv.skilltable.skilltree[conv.skilltable.skilltree["SkillName"]==skillname].head(1)
    skill=Skill()
    skill.description=conv.dictable.krtojp(pa["Caption"].item())
    skill.caption2 = conv.dictable.krtojp(pa["Caption2"].item())
    skill.classname=pa["ClassName"].item()
    skill.clsid=pa["ClassID"].item()
    skill.maxlv=pt["MaxLevel"].item()
    skill.reqlv=pt["UnlockClassLevel"].item()
    skill.iconname="icon_"+pa["Icon"].item()
    skill.name= conv.dictable.krtojp(pa["Name"].item())
    skill.attributes=[]
    for attr in conv.skilltable.ability[conv.skilltable.ability["SkillCategory"]==skillname].iterrows():

        att=generateAttribute(conv,job,attr[1])
        if att is not None:
            #print(skillname)
            skill.attributes.append(att)
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
    job.name = re.sub("\{.*?\}","",conv.dictable.krtojp(jobdata["Name"]))
    job.engname = jobdata["EngName"]
    job.STR = jobdata["STR"]
    job.CON = jobdata["CON"]
    job.INT = jobdata["INT"]
    job.SPR = jobdata["MNA"]
    job.DEX = jobdata["DEX"]
    job.rank= jobdata["Rank"]
    job.ctrltype=ctrltype[jobdata["CtrlType"]]
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
    job.attributes=[]
    for attr in conv.skilltable.ability.iterrows():
        if(attr[1]["SkillCategory"]=="All"):
            att=generateAttribute(conv,job,attr[1])
            if(att is not None):
                job.attributes.append(att)
    job.skills=[]
    # skills
    for skillintree in filter(lambda x:re.match("^"+job.classname+"_",x[1]["ClassName"]),conv.skilltable.skilltree.iterrows()):
        job.skills.append(generateSkills(conv,job,skillintree[1]["SkillName"]))
    return job
def generateJobTree(conv:DicConverter):
    tree=JobTree()
    for j in conv.skilltable.job.iterrows():
        #print(j[1]["EngName"])
        tree.jobs.append(generateJob(conv,j[1]))

    return tree