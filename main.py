
import DicTable
import SkillTable
import TosStructure
import DicConverter
import OptTable
import ToWiki
import TosImage
import os
import re
def dicprocess():
    dt = DicTable.DicTable("./data")
    st = SkillTable.SkillTable("./data")
    opt = OptTable.OptTable("./data")
    tree = TosStructure.generateJobTree(DicConverter.DicConverter(dt, st, opt))
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
        imdic[img.name]=img
    for job in tree.jobs:
        for attr in job.attributes:
            if attr.iconname in imdic:
                img=imdic[attr.iconname]

                img.extractIcon("./data","./out/skillbyicon","ICO_"+ensure(attr.name))
                print(attr.name)
        for skill in job.skills:
            if skill.iconname in imdic:
                img = imdic[skill.iconname]
                img.extractIcon("./data", "./out/skillbyicon", "ICO_" + ensure(skill.name))
                print(skill.name)
            for attr in skill.attributes:
                if attr.iconname in imdic:
                    img = imdic[attr.iconname]
                    img.extractIcon("./data", "./out/skillbyicon", "ICO_" + ensure(attr.name))
                    print(attr.name)

def main():
    if not os.path.exists("./out"):
        os.mkdir("./out")
    print("TosBaseDataGenerator by ebisuke")
    tree=dicprocess()
    print("Extract Icons")
    imgprocess(tree)
    print("Completed")
if __name__ == "__main__":
    main()
