from DicTable import DicTable
from SkillTable import SkillTable
from OptTable import OptTable
class DicConverter:
    dictable:DicTable=None
    skilltable:SkillTable=None
    opttable:OptTable=None
    def __init__(self,dictable,skilltable,opttable):
        self.dictable=dictable
        self.skilltable=skilltable
        self.opttable=opttable