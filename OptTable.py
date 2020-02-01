
import json
import xml.etree.ElementTree as ET
import re
import glob
import pandas

class OptTable:
    opt=None

    def __init__(self, path):
        self.path = path
        self.opt=pandas.read_excel(path+"/opts.xlsx",dtype=str,keep_default_na=False, na_values="")