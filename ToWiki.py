import TosStructure
import OptTable
import re
import datetime
docbase="""{{Infobox Class|%ctrltype%||%classmaster%|||%classtype%|%attackproperty%
| str=%str% 
| dex=%dex% 
| con=%con% 
| int=%int% 
| spr=%spr% 
}}
%description%

==伝承==
%lores%

==背景==
%background%
==アイコンとコスチューム==
%iconandoutfits%
==スキルと特性==
<tabber>
Tree View=
{| class="wikitable"
|+
!Unlock
%treeviewlevels%
|-
%treeviewcells%
|-
%treeviewrows%
|}
|-|
List View=
{| class="wikitable"
%listviewskills%
|}

{| class="wikitable" border="1" cellpadding="1" cellspacing="1" style="width: 800px;"
{{ListViewAttribute}}
%listviewattributes%
|-
{{ListViewArts}}
%listviewarts%
|}
</tabber>

==クラス関係==
<tabber>
適合=
{{ClassTable|%fullcompatibilityclasses%}}
|-|
部分的に適合=
{{ClassTable|%partialcompatibilityclasses%}}
|-|
特殊作用=
{{ClassTable|%specialeffectclasses%}}
|-|
類似=
{{ClassTable|%similarclasses%}}
</tabber>

==Tipsと戦略==
%tips%

==ギャラリー==
%gallery%

==トリビア==
%trivia%

==参照==
{{Reflist}}

==外部リンク==
%externallink%
{{ClassFooter|%ctrltype%}}
==履歴==
* Automatic generated at %date%
{{PageProgress|2}}
"""
def replacenl(s):
    return s.replace("\n","<br/>").replace("{nl}","<br/>")
def rb(s):
    return re.sub("{.*?}","",s)

#return levels cells rows
def generateTreeView(job:TosStructure.Job):
    levels=""
    maxlevels={}
    for skill in job.skills:
        if(not skill.maxlv in maxlevels):
            maxlevels[skill.maxlv]=1
        else:
            maxlevels[skill.maxlv] +=1

    ll=[]
    for k,v in maxlevels.items():
        ll.append({"k":k,"v":v})

    ll.sort(key=lambda x:x["k"],reverse=True)
    #for v in ll:
    #     levels+="{{TreeViewRow|$|%d|%d}}\n" % (v["k"] , v["v"])

    skills=job.skills
    skills.sort(key=lambda x: x.reqlv,reverse=False)

    reqlv=0
    cells=""
    for v in skills:
        s:TosStructure.Skill=v
        if(reqlv!=s.reqlv):
            cells+="|-\n! Lv"+str(s.reqlv)+"\n"
            reqlv=s.reqlv
        cell=s.name
        for c in s.attributes:

            a:TosStructure.Attribute = c
            m=re.match("(\[アーツ\]|)"+s.name+"[：|\:](.*)$",a.name)
            if(m is not None):
                cell+="|"+m.group(2)
        cells+="{{TreeViewCell|"+cell+"}}<br/><br/>\n"

    rows="{{TreeViewRow|"
    for c in job.attributes:
        a: TosStructure.Attribute = c
        m = re.match("(\[アーツ\]|)" + "[：|\:](.*)$", a.name)
        if (m is not None):
            rows += "|" + m.group(2)
    rows+="}}\n"
    return levels,cells,rows
def generateListView(job:TosStructure.Job):
    skills = job.skills
    skills.sort(key=lambda x: x.reqlv)
    reqlv=0
    lvs=1
    listview=""
    for v in skills:
        s: TosStructure.Skill = v
        if (reqlv != s.reqlv):
            listview+= "{{ListViewSkill|%d}}\n|-\n" % lvs
            reqlv = s.reqlv
            lvs+=1
        m=re.search("\{#\d*?\}\{ol\}(.*?)\{/\}\{/\}(.*)$",s.description)
        typ=""
        desc=""
        if(m is not None):
            typ=m.group(1)
            desc=m.group(2)
        else:
            typ=" . "
            desc=s.description

        vv="{{ListViewSkill|"+s.name+"|"+typ+"|"+replacenl(rb(desc))+"|"+str(s.maxlv)+"}}\n"
        listview+=vv
    return listview
def generateAttribute(job:TosStructure.Job):
    att=""
    for at in job.attributes:
        a:TosStructure.Attribute = at

        if(a.arts==False):
            m=re.search("(.*?)：(.*)$",a.name)
            attrname=""
            attreffect=""
            if(m is not None):
                attrname=m.group(1)
                attreffect = m.group(2)
            else:
                attrname=a.name
            desc=replacenl(a.description)
            att+="{{ListViewAttribute|"+attrname+"|"+attreffect+"|"+str(a.reqlv)+"|"+str(a.maxlv)+"|"+rb(replacenl(desc))+"}}\n"
    for sk in job.skills:
        s: TosStructure.Skill = sk
        for a in s.attributes:
            if (a.arts == False):
                m = re.search("(.*?)：(.*)$", a.name)
                attrname = ""
                attreffect = ""
                if (m is not None):
                    attrname = m.group(1)
                    attreffect = m.group(2)
                else:
                    attrname = a.name
                desc = replacenl(a.description)
                attrname = re.sub("[:|：]", " - ", attrname)
                attreffect = re.sub("[:|：]", " - ", attreffect)
                att += "{{ListViewAttribute|" + attrname + "|" + attreffect + "|" + str(a.reqlv) + "|" + str(
                    a.maxlv) + "|" + rb(replacenl(desc)) + "}}\n"

    return att
def generateArtsAttribute(job:TosStructure.Job):
    att=""
    for at in job.attributes:
        a:TosStructure.Attribute = at
        if(a.arts==True):
            an=a.name.replace("[アーツ]","")
            an=re.sub("[:|：]"," - ",an)
            desc=replacenl(a.description)
            att+="{{ListViewArts|"+an+"|"+replacenl(rb(desc)) +"}}\n"
    for sk in job.skills:
        s: TosStructure.Skill = sk
        for a in s.attributes:
            if (a.arts == True):
                an = a.name.replace("[アーツ]", "")
                an=re.sub("[:|：]"," - ",an)
                desc = replacenl(a.description)
                att += "{{ListViewArts|" + an + "|" + replacenl(rb(desc)) + "}}\n"

    return att
def stringnizeJob(job:TosStructure.Job,opt:OptTable.OptTable):
    op=opt.opt[opt.opt["JobName"]==job.engname]
    tlevel,tcell,trow=generateTreeView(job)
    listview=generateListView(job)
    attrview=generateAttribute(job)
    artsview=generateArtsAttribute(job)
    doc=docbase\
    .replace("%ctrltype%",str(job.ctrltype))\
    .replace("%classmaster%",job.classmaster)\
    .replace("%classtype%",str(op["ClassType"].item()))\
    .replace("%attackproperty%",str(op["AttackProperty"].item())) \
    .replace("%str%", str(job.STR)) \
    .replace("%dex%", str(job.DEX)) \
    .replace("%con%", str(job.CON)) \
    .replace("%int%", str(job.INT)) \
    .replace("%spr%", str(job.SPR)) \
    .replace("%description%", job.description)\
    .replace("%lores%",job.lores)\
    .replace("%background%",str(op["Background"].item()))\
    .replace("%iconandoutfits%", str(op["IconAndOutfits"].item())) \
    .replace("%treeviewlevels%", tlevel) \
    .replace("%treeviewcells%", tcell) \
    .replace("%treeviewrows%", trow) \
    .replace("%listviewskills%", listview) \
    .replace("%listviewattributes%", attrview) \
    .replace("%listviewarts%", artsview) \
    .replace("%fullcompatibilityclasses%",str( op["FullCompatibilityClasses"].item()))\
    .replace("%partialcompatibilityclasses%",str( op["PartialCompatibilityClasses"].item()))\
    .replace("%specialeffectclasses%", str(op["SpecialEffectClasses"].item()))\
    .replace("%similarclasses%", str(op["SimilarClasses"].item()))\
    .replace("%tips%", str(op["Tips"].item()))\
    .replace("%gallery%",str(op["Gallery"].item()))\
    .replace("%trivia%", str(op["Trivia"].item())) \
    .replace("%externallink%", str(op["ExternalLink"].item())) \
    .replace("%date%", str(datetime.datetime.now()))

    return doc
def exportJob(path,job,opt:OptTable.OptTable):
    with open(path+"/job_"+job.engname+".txt","w",encoding="utf-8") as f:
        f.write(stringnizeJob(job,opt))
def exportJobTree(path,jobtree:TosStructure.JobTree,opt:OptTable.OptTable):
    for job in jobtree.jobs:
        exportJob(path,job,opt)
    with open(path+"/joblist.txt","w",encoding="utf-8") as f:
        f.write("jobname,filename\n")
        for job in jobtree.jobs:
            if(job.rank==2):
                f.write(job.name+","+"job_"+job.engname+".txt"+"\n")