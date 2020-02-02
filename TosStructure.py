from DicConverter import DicConverter
import pandas
import re
import TosFunc as tf
ctrltype={
    "Warrior":4,
    "Scout":3,
    "Wizard":5,
    "Cleric":2,
    "Archer":1,
}


class JobTree:
    jobs=[]
    def getJobByName(self,s):
        for j in self.jobs:
            if(j.name==s):
                return s
        return None
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
class SkillCaption:
    # prefix=""
    # title=""
    # caption=""
    # prefix2 = ""
    # caption2=None
    # suffix=""
    # value=[]
    # value2 = []

    vars=[]
    texts=[]
    realvars=[[]]
    def __st(self,v):
        return "%2g" % v
    def __init__(self,s):

        vars=re.findall("#{(.*?)}#",s)
        texts=re.split("(#{.*?}#)",s)
        texts=[v for v in texts if not v.startswith("#{")]
        self.vars=vars
        self.texts = texts
        self.realvars=[[] for v in vars]
    def isNumberStarted(self):
        if len(self.texts)>0 and re.match("^\d",self.texts[0])!=None:
            return True
        return False
    def getTitle(self):
        if len(self.texts)>0 and len(self.vars)>0:
            if self.vars[0]=="SkillFactor":
                return self.texts[0]
            else:
                if not self.isNumberStarted():

                    return self.texts[0]
                else:
                    if len(self.vars) == 1:
                        return self.texts[0]
                    if len(self.realvars[0])>0:
                        if len(self.texts) > 1:
                            return self.texts[0]+tf.ns(self.realvars[0][0])+ self.texts[1]
                        else:
                            return self.texts[0] + tf.ns(self.realvars[0][0])
                    else:
                        if len(self.texts) > 1:
                            return self.texts[0]+self.vars[0]+ self.texts[1]
                        else:
                            return self.texts[0] + self.vars[0]
        if(len(self.texts)>0):
            return self.texts[0]

    def getContent(self, lvidx):
        if len(self.texts) > 0 and len(self.vars) > 0:
            if self.vars[0] == "SkillFactor":
                #sfr weaving
                s=""
                for i in range(0,len(self.realvars)):

                    s +=tf.ns(self.realvars[i][lvidx])
                    s += self.texts[i+1]
                #s += self.texts[len(self.realvars)]
                return s
            else:
                # after sfr weaving
                s = ""
                startidx=0
                if self.isNumberStarted():
                   startidx=1
                for i in range(startidx, len(self.realvars) ):

                    s += tf.ns(self.realvars[i][lvidx])
                    s += self.texts[i + 1]
                return s

        return ""

        # title=re.sub("^\*","",title)
        #
        # self.title=tf.removestuff(title)
        # self.caption = tf.removestuff(caption)
        # self.caption2=None
        # self.suffix = tf.removestuff(suffix)
        # self.value=[]
        # self.value2 = []
        # m=re.search("(.*?)(アップ|上昇|増加|追加)",suffix)
        # if(m!=None):
        #     self.prefix="+"
        #     self.suffix=m.group(1)
        # m = re.search("(.*?)(ダウン|減少|下降)",suffix)
        # if(m!=None):
        #     self.prefix = "-"
        #     self.suffix = m.group(1)
        #
        # m = re.search("(.*?)#\{(.*?)\}#(.*)$",suffix)
        #
        # if (m != None):
        #     suf2=m.group(3)
        #     if(len(suf2)>4):
        #         self.prefix2 = m.group(1)+" n"+suf2
        #         self.caption2 = m.group(2)
        #         self.suffix = ""
        #     else:
        #         self.prefix2=m.group(1)
        #         self.caption2 = m.group(2)
        #         self.suffix=m.group(3)
    def tostr(self,lvidx):
        # weaving
        return self.getContent(lvidx)

        # if(self.caption2==None):
        #     return self.prefix+"{:2g}".format(self.value[idx])+self.suffix
        # else:
        #     return self.prefix + "{:2g}".format(self.value[idx]) + self.prefix2 + "{:2g}".format(self.value2[idx]) + self.suffix

class Skill:
    description=""
    caption2=""
    sp=[]
    cd=[]
    oh=0
    classname=""
    clsid=0
    name=""
    maxlv=None
    reqlv=0
    iconname=""
    captiontime=[]
    captionratio=[]
    captionratio2 = []
    variables=[]
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
    attr.name=tf.removestuff(conv.dictable.krtojp(attrdata["Name"]))
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
    skill.sp = []
    skill.cd = []
    skill.classname=pa["ClassName"].item()
    skill.clsid=pa["ClassID"].item()
    skill.maxlv=pt["MaxLevel"].item()
    skill.reqlv=pt["UnlockClassLevel"].item()
    skill.iconname="icon_"+pa["Icon"].item()
    skill.name= conv.dictable.krtojp(pa["Name"].item())
    skill.variables=[]
    for s in skill.caption2.split("{nl}"):

        # SFR First

        # m=re.search("(.*?)#\{(.*?)\}#(.*)$",s)

        skill.variables.append(SkillCaption(s))

    skill.attributes=[]
    for attr in conv.skilltable.ability[conv.skilltable.ability["SkillCategory"]==skillname].iterrows():

        att=generateAttribute(conv,job,attr[1])
        if att is not None:
            #print(skillname)
            skill.attributes.append(att)
    return skill
def findMasterName(conv,jobjpname):
    for k,v in  conv.dictable.dicidtojp:
        m=re.search("")
def generateJob(conv: DicConverter, jobdata:Job):
    job=Job()
    job.clsid = jobdata["ClassID"]
    job.classname = jobdata["ClassName"]
    job.name = tf.removestuff(conv.dictable.krtojp(jobdata["Name"]))
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

        job.description=tf.removestuff(m.group(2))
        job.lores=tf.removestuff(m.group(1))
    else:
        job.description=tf.removestuff(desc)
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
        #if j[1]["EngName"]=="Exorcist":
        tree.jobs.append(generateJob(conv,j[1]))
        #break
    return tree