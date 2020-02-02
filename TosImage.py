import xml.etree.ElementTree as ET
import re
import PIL.Image as Image
class TosImage:
    name=""
    # x,y,w,h
    bounds=(0,0,0,0)
    file=""

    def extractIcon(self,srcpath,dstpath,anothername=None):
        #ファイル名はすべてpng
        try:
            im=Image.open(srcpath+"/"+self.file)
            #slice
            dst=im.crop((self.bounds[0],self.bounds[1],self.bounds[0]+self.bounds[2],self.bounds[1]+self.bounds[3]))
            #dst=im[self.bounds[0]:self.bounds[2]+self.bounds[0],self.bounds[1]:self.bounds[3]+self.bounds[1]]
            #save
            if anothername==None:
                dst.save(dstpath+"/"+self.name+".png")
            else:
                dst.save(dstpath + "/" + anothername + ".png")
        except FileNotFoundError:
            print("File not found.")
def parseTosImageXml(path):
    tree=ET.parse(path)
    root=tree.getroot()
    tosimages=[]
    for imagelist in root:
        for image in imagelist:
            ti=TosImage()

            ti.name=image.attrib["name"].lower()
            ti.file = image.attrib["file"].lower()
            m=re.match("(\d+?)\s+?(\d+?)\s+?(\d+?)\s+?(\d+)",image.attrib["imgrect"])
            ti.bounds=(int(m.group(1)),int(m.group(2)),int(m.group(3)),int(m.group(4)))
            tosimages.append(ti)
    return tosimages

