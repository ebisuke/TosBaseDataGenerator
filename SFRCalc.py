import lupa
import TosStructure
import SkillTable
import os
import glob
class SFRCalc:
    table:SkillTable.SkillTable=None
    lua=None
    def __init__(self,table:SkillTable.SkillTable):
        self.table=table
        self.lua = lupa.LuaRuntime(register_eval=True,unpack_returned_tuples=True)


        for fp in glob.glob("./data/shared.ipf/script/*.lua",recursive=True):
            with open(fp, "r",encoding="utf-8-sig",errors='ignore') as f:
                s = f.read()
                print(fp)
                self.lua.execute(s)
        with open("./sfrbase.lua", "r", encoding="utf-8") as f:
            s = f.read()
            self.lua.execute(s)

    def getSkillByName(self, name):
        #print(name)
        return self.table.skill[self.table.skill["ClassName"] == name].to_dict(orient="records")[0]
    def getSkillArgByName(self,clsid,name):
        if(name!=None):
            inter=self.table.skill[self.table.skill["ClassID"]==clsid]
            nam=inter[name]
            #print(str(clsid)+":"+name)
            return inter[name].head(1).item()
        return None
    def CalcCaption(self,captionname,clsid,level):
        return self.lua.eval("function (self,captionname,clsid,level) "
                             "return CalcCaption(self,captionname,clsid,level);"
                             "end")(self,captionname,clsid,level)
    def CalcValue(self,prop,clsid,level):
        return self.lua.eval("function (self,captionname,clsid,level) "
                             "return CalcValue(self,captionname,clsid,level);"
                             "end")(self,prop,clsid,level)


