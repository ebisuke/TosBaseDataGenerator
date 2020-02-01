import TosStructure
import OptTable
import re
docbase="""
{{Infobox Class|%ctrltype%||%classmaster%|||%classtype%|%attackproperty%
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
{{ClassTable|%fullcompatiblityclasses%}}
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
{{ClassFooter|2}}
==履歴==
* Automatic generated
{{PageProgress|2}}
"""
def replacenl(s):
    return str.replace(s,"{nl}","\n")
#return levels cells rows
def generateTreeView(job:TosStructure.Job):
    levels=""
    maxlevels={}
    for skill in job.skills:
        if(not skill.maxlv in maxlevels):
            maxlevels[skill.maxlv]=1
        else:
            maxlevels[skill.maxlv] +=1
    for k,v in maxlevels:
        levels+=str.format("{{TreeViewRow|$|%d|%d}}\n",k,v)

    skills=job.skills
    skills.sort(key=lambda x: x.unlocklv)

    reqlv=0
    cells=""
    for v in skills:
        s:TosStructure.Skill=v
        if(reqlv!=s.unlocklv):
            cells+="! Lv"+str(s.unlocklv)
            reqlv=s.unlocklv
        cell=s.name
        for c in s.attributes:
            a:TosStructure.Attribute = c
            m=re.match("(\[アーツ\]|)"+s.name+"：(.*)$",a.name)
            if(m is not None):
                cell+="|"+m.group(2)
        cells+="{{TreeViewCell|"+cell+"}}<br/><br/>"

    rows="{{TreeViewRow|"
    for c in job.attributes:
        a: TosStructure.Attribute = c
        m = re.match("(\[アーツ\]|)" + "：(.*)$", a.name)
        if (m is not None):
            rows += "|" + m.group(2)
    rows+="}}"
    return levels,cells,rows
def generateListView(job:TosStructure.Job):
    skills = job.skills
    skills.sort(key=lambda x: x.unlocklv)
    reqlv=0
    lvs=1
    listview=""
    for v in skills:
        s: TosStructure.Skill = v
        if (reqlv != s.unlocklv):
            listview+= str.format("{{ListViewSkill|%d}}\n|-",lvs)
            reqlv += s.unlocklv
            lvs+=1
        m=re.search("\{#\d*?\}\{ol\}(.*?)\{/\}\{/\}(.*)$",s.description)
        typ=""
        desc=""
        if(m is not None):
            typ=m.group(1)
            desc=m.group(2)
        else:
            desc=s.description
        vv="{{ListViewSkill|"+s.name+"|"+typ+"|"+replacenl(desc)+"|"+s.maxlv+"}}\n"
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
            att+="{{ListViewAttribute|"+attrname+"|"+attreffect+"|"+str(a.reqlv)+"|"+str(a.maxlv)+"|"+desc+"}}"
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
                att += "{{ListViewAttribute|" + attrname + "|" + attreffect + "|" + str(a.reqlv) + "|" + str(
                    a.maxlv) + "|" + desc + "}}"

    return att
def generateArtsAttribute(job:TosStructure.Job):
    att=""
    for at in job.attributes:
        a:TosStructure.Attribute = at
        if(a.arts==True):
            an=a.name.replace("[アーツ]","")
            an=an.replace("："," - ")
            desc=replacenl(a.description)
            att+="{{ListViewArts|"+an+"|"+desc+"}}"
    for sk in job.skills:
        s: TosStructure.Skill = sk
        for a in s.attributes:
            if (a.arts == True):
                an = a.name.replace("[アーツ]", "")
                an = an.replace("：", " - ")
                desc = replacenl(a.description)
                att += "{{ListViewArts|" + an + "|" + desc + "}}"

    return att
def stringnizeJob(job:TosStructure.Job,opt:OptTable.OptTable):
    op=opt.opt[opt.opt["ClassName"]==job.engname]
    tlevel,tcell,trow=generateTreeView(job)
    listview=generateListView(job)
    attrview=generateAttribute(job)
    artsview=generateArtsAttribute(job)
    doc=docbase\
    .replace("%ctrltype%",job.ctrltype)\
    .replace("%classmaster%",job.classmaster)\
    .replace("%classtype%",opt.opt["ClassType"])\
    .replace("%attackproperty%",opt.opt["AttackProperty"]) \
    .replace("%str%", str(job.STR)) \
    .replace("%dex%", str(job.DEX)) \
    .replace("%con%", str(job.CON)) \
    .replace("%int%", str(job.INT)) \
    .replace("%spr%", str(job.SPR)) \
    .replace("%description%", job.description)\
    .replace("%lores%",job.lores)\
    .replace("%background%",opt["Background"])\
    .replace("%iconandoutfits%", opt["IconAndOutFits"]) \
    .replace("%treeviewlevels%", tlevel) \
    .replace("%treeviewcells%", tcell) \
    .replace("%treeviewrows%", trow) \
    .replace("%listviewskills%", listview) \
    .replace("%listviewattributes%", attrview) \
    .replace("%listviewarts%", artsview) \
    .replace("%fullcompatiblityclasses%", opt["FullCompatiblityClasses"])\
    .replace("%partialcompatibilityclasses%", opt["PartialCompatibilityClasses"])\
    .replace("%specialeffectclasses%", opt["SpecialEffectClasses"])\
    .replace("%similarclasses%", opt["SimilarClasses"])\
    .replace("%tips%", opt["tips"])\
    .replace("%gallery%", opt["gallery"])\
    .replace("%trivia%", opt["trivia"]) \
    .replace("externallink", opt["externallink"])

def exportJob(path,job,opt:OptTable.OptTable):
    with open(path+"/job_"+job.engname+".txt","w") as f:
        f.write(stringnizeJob(job,opt))
def exportJobTree(path,jobtree:TosStructure.JobTree,opt:OptTable.OptTable):
    for job in jobtree.jobs:
        exportJob(path,job)