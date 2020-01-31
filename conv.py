
import DicTable
import SkillTable
import TosStructure
import DicConverter
def main():
    dt=DicTable.DicTable("./data")
    st=SkillTable.SkillTable("./data")
    tree=TosStructure.generateJobTree(DicConverter.DicConverter(dt,st))
if __name__ == "__main__":
    main()