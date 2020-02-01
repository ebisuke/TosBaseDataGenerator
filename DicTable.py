
import json
import xml.etree.ElementTree as ET
import re
import glob
import pandas
class DicTable:

    dicidtojp={}
    krtodicid={}
    dicidtokr = {}
    path=""
    def __init__(self,path):
        self.path=path
        self.parseKrDic()
        self.parseJpDic()
    def parseJpDic(self):
        list=glob.glob(self.path+"/Japanese/*.tsv")
        for file in list:
            with open(file,encoding="utf-8") as f:
                lines=f.readlines()
                l=0
                for line in lines:
                    m = re.search("(.*?)\t(.*?)(\t|$)", line)
                    l+=1
                    if( m is not None):
                        self.dicidtojp[m.group(1)]=m.group(2)
                    m = re.search("(.*?)\t(.*?)\t(.*?)(\t|$)", line)
                    if( m is not None):
                        self.dicidtokr[m.group(1)]=m.group(3)
                        self.krtodicid[m.group(3)] = m.group(1)

    def parseKrDic(self):
        tree = ET.parse(self.path+"/"+"wholeDicID.xml")
        root = tree.getroot()
        for file in root:
            for data in file:
                txt=data.attrib["dicid"]
                m=re.search("@dicID_\^\*\$(.*?)\$\*\^",txt)
                self.krtodicid[data.attrib["original"]]=m.group(1)
                self.dicidtokr[m.group(1)] = data.attrib["original"]
        tree = ET.parse(self.path+"/"+"DicIDTable.xml")
        root = tree.getroot()
        for data in root:

            txt=data.attrib["ID"]
            self.krtodicid[data.attrib["kr"]]=txt
            self.dicidtokr[txt] = data.attrib["kr"]
    def krtojp(self,kr):
        if(isinstance(kr,pandas.Series)):
            if(pandas.Series.isnull(kr)):
                return ""

        if(kr==kr):
            if(kr in self.krtodicid ):
                return self.dicidtojp[self.krtodicid[kr]]
            else:
                return kr
        else:
            return ""