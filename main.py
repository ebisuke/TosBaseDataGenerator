
import DicTable
import SkillTable
import TosStructure
import DicConverter
import OptTable
import ToWiki
def main():
    dt=DicTable.DicTable("./data")
    st=SkillTable.SkillTable("./data")
    opt=OptTable.OptTable("./data")
    tree=TosStructure.generateJobTree(DicConverter.DicConverter(dt,st,opt))
    ToWiki.exportJobTree("./out",tree,opt)
if __name__ == "__main__":
    main()
