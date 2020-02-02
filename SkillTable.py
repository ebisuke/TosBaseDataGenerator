import pandas
import glob
import re
class SkillTable:
    map={}
    skill={}
    job={}
    ability={}
    abilityjob={}
    skilltree={}
    path = ""
    def __init__(self, path):
        self.path = path
        self.parse()

    def getSkillArgByName(self,clsid,name):
        return self.table[self.table["ClassID"]==clsid].item()[name]
    def parse(self):
        self.skill=pandas.read_csv(self.path+"/skill.ies",encoding="utf-8")
        self.job = pandas.read_csv(self.path + "/job.ies", encoding="utf-8")
        self.map = pandas.read_csv(self.path + "/map.ies", encoding="utf-8")
        self.skilltree = pandas.read_csv(self.path + "/skilltree.ies", encoding="utf-8")
        self.ability = pandas.read_csv(self.path + "/ability.ies", encoding="utf-8")
        list = glob.glob(self.path + "/ability_*.ies")
        for file in list:
            m = re.search("ability_(.*?)\.ies", file)
            abilname=m.group(1)
            self.abilityjob[abilname]= pandas.read_csv(file, encoding="utf-8")