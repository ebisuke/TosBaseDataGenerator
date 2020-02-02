import lupa
import TosStructure
import SkillTable
import os
import glob
import pandas
class SFRCalc:
    table:SkillTable.SkillTable=None
    lua=None
    funcalcvalue=None
    funcalcoh = None
    funcalccaption = None

    def __init__(self,table:SkillTable.SkillTable):
        self.table=table
        self.lua = lupa.LuaRuntime(register_eval=True,unpack_returned_tuples=True)
        self.funcalccaption=self.lua.eval(
                            "function (self,captionname,clsid,level) "+
                             "return CalcCaption(self,captionname,clsid,level);"+
                             "end")
        self.funcalcoh = self.lua.eval(
            "function (self,clsid,level) "+
             "return CalcOH(self,clsid,level);"+
             "end")
        self.funcalcvalue = self.lua.eval(
            "function (self,prop,clsid,level) "+
             "return CalcValue(self,prop,clsid,level);"
             "end")
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
            if not pandas.isna(inter[name].head(1).item()):
                return inter[name].head(1).item()
            else:
                return None
        return None
    def CalcCaption(self,captionname,clsid,level):
        return self.funcalccaption(self,captionname,clsid,level)
    def CalcValue(self,prop,clsid,level):
        return self.funcalcvalue(self,prop,clsid,level)

    def CalcOH(self,clsid,level):
        return self.funcalcoh(self,clsid,level)

