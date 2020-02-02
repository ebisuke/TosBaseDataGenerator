
import DicTable
import SkillTable
import TosStructure
import DicConverter
import OptTable
import ToWiki
import TosImage
import os
import re
import SFRCalc
import joblib
import copy
def dicprocess():
    dt = DicTable.DicTable("./data")
    st = SkillTable.SkillTable("./data")
    opt = OptTable.OptTable("./data")

    tree = TosStructure.generateJobTree(DicConverter.DicConverter(dt, st, opt))
    sfrc = SFRCalc.SFRCalc(st)
    # calc sfr

    for j in tree.jobs:
        print(j.name)
        for s in j.skills:
            s.oh=sfrc.CalcOH(s.clsid,s.maxlv)
            if(s.oh==0):
                s.oh=1

            s.cd.append(sfrc.CalcValue("CoolDown", s.clsid, 1) / 1000.0)
            s.sp.append(sfrc.CalcValue("SpendSP", s.clsid, s.maxlv))
            for c in s.variables:
                for lv in range(1,s.maxlv+1):
                    c.value.append(sfrc.CalcCaption(c.caption,s.clsid, lv))
                    if(c.caption2!=None):
                        c.value2.append(sfrc.CalcCaption(c.caption2, s.clsid, lv))
    ToWiki.exportJobTree("./out", tree, opt)
    return tree
def ensure(name):
    return re.sub("\{.*?\}","",re.sub("\[アーツ\]","",re.sub("[\:|：]"," - ",name)))

def imgprocess(tree):
    ti=[]
    #ti.extend(TosImage.parseTosImageXml("./data/itemicon.xml"))
    ti.extend(TosImage.parseTosImageXml("./data/skillicon.xml"))
    #save
    if not os.path.exists("./out/icon"):
        os.mkdir("./out/icon")
    if not os.path.exists("./out/skillbyicon"):
        os.mkdir("./out/skillbyicon")

    for img in ti:
        img.extractIcon("./data","./out/icon")
        print(img.name)
    # dictonary
    imdic={}
    for img in ti:
        imdic[img.name.lower()]=img
    for job in tree.jobs:
        for attr in job.attributes:
            if attr.iconname.lower() in imdic:
                img=imdic[attr.iconname.lower()]
                img.extractIcon("./data","./out/skillbyicon","ICO_"+ensure(attr.name))
                print(attr.name)
        for skill in job.skills:
            if skill.iconname.lower() in imdic:
                img = imdic[skill.iconname.lower()]
                img.extractIcon("./data", "./out/skillbyicon", "ICO_" + ensure(skill.name))
                print(skill.name)
            for attr in skill.attributes:
                if attr.iconname.lower() in imdic:
                    img = imdic[attr.iconname.lower()]
                    img.extractIcon("./data", "./out/skillbyicon", "ICO_" + ensure(attr.name))
                    print(attr.name)

def main():
    if not os.path.exists("./out"):
        os.mkdir("./out")
    print("TosBaseDataGenerator by ebisuke")
    tree=dicprocess()
    #print("Extract Icons")
    #imgprocess(tree)
    print("Completed")
if __name__ == "__main__":
    main()
