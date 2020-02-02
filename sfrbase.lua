-- dummies
ui={
     GetFrame=function(str)
          return {
               IsVisible=function()
                    return 0
               end
          }
     end
}
session={
     party={
          GetPartyMemberList=function (typ)
               return nil
          end
     }
}
globalself={}
function GetSkill(self,clsid,level)
     self=globalself
     if(type(clsid)=="number")then
          return {
               SklFactor=tonumber(self:getSkillArgByName(clsid,"SklFactor")),
               SklFactorByLevel=tonumber(self:getSkillArgByName(clsid,"SklFactorByLevel")),
               Level=level,
               ClassName=self:getSkillArgByName(clsid,"ClassName"),
               BasicSP=tonumber(self:getSkillArgByName(clsid,"BasicSP")),
               SklSR=tonumber(self:getSkillArgByName(clsid,"SklSR")),
               SpendItemBaseCount=tonumber(self:getSkillArgByName(clsid,"SpendItemBaseCount")),
               LvUpSpendPoison=tonumber(self:getSkillArgByName(clsid,"LvUpSpendPoison")),
               BasicPoison=tonumber(self:getSkillArgByName(clsid,"BasicPoison")),
               BasicCoolDown=tonumber(self:getSkillArgByName(clsid,"BasicCoolDown")),
               MinCoolDown=tonumber(self:getSkillArgByName(clsid,"MinCoolDown")),
               BasicSta=tonumber(self:getSkillArgByName(clsid,"BasicSta")),
               SklUseOverHeat=tonumber(self:getSkillArgByName(clsid,"SklUseOverHeat")),
          }
     else

          return self:getSkillByName(clsid)
     end
end
function GetExProp(pc, state)
     return 0
end
function TryGetProp(self,str)

     local table={
          Lv=300,
          STR=300,
          CON=300,
          DEX=300,
          INT=300,
          MNA=300,
          ReinforceAbility="None"
     }
     return self[str] or table[str] or "None"
end
function IsBuffApplied(pc,name)
     return "NO"
end
function GetZoneName(pc)
     return "c_siauliai"
end
function GetAbilityAddSpendValue(pc,skillname,status)
     local table={
          SpendItem=0,
          SP=0,
          CoolDown=0,

     }
     return 0
end
function GetClassList(skill)
     return globalself
end
function GetSkillOwner(skill)
     return {
          -- AOE
          SR=0,
          MINMATK=10000,
          MINPATK=10000,
          MAXMATK=10000,
          MAXPATK=10000,
          MINMATK_SUB=10000,
          MINPATK_SUB=10000,
          MAXMATK_SUB=10000,
          MAXPATK_SUB=10000,
          MHP=100000,
          MHP_BM=100000,
          Lv=300,
          STR=300,
          CON=300,
          DEX=300,
          INT=300,
          MNA=300,
     }
end
function GetAbility(skill)
     return nil
end


function GetSumValueByItem(pc,skill,name)
     return pc[name]+skill[name]
end
function IsPVPServer()
     return 0
end
function IsPVPField()
     return 0
end
function IsRaidField()
     return 0
end
function IsServerObj(pc)
     return 0
end
function IsServerSection(pc)
     return 0
end
function GetMyJobHistoryString()
     return ""
end
function GetJobHistoryString()
     return ""
end
function IS_PC(pc)
     return true
end
function IsBattleState(pc)
     return 0
end
function GetClassByNameFromList(cls,classname)
     return globalself.getSkillByName(classname)
end
function SCR_GET_SPEND_ITEM_Alchemist_SprinkleHPPotion()
     return {NumberArg1=802}
end
function SCR_GET_SPEND_ITEM_Alchemist_SprinkleSPPotion()
     return {NumberArg1=184}
end
function CalcCaption(self,caption,clsid,level)
     -- acq sfr
     local sfrscr=self:getSkillArgByName(clsid,caption)
    globalself=self
     --local tooltipattr=self:getSkillArgByName(clsid,"Tooltip_Attr")
     if(sfrscr==nil)then
          return nil
     end

     return _G[sfrscr](GetSkill(self,clsid,level))


end
function CalcValue(self,prop,clsid,level)
     -- acq sfr
     local sfrscr=self:getSkillArgByName(clsid,prop)
     globalself=self
     if(sfrscr==nil or sfrscr=="" or sfrscr=="nan")then
          return nil
     end
     return _G[sfrscr](GetSkill(self,clsid,level))
end
function CalcOH(self,clsid,level)
     -- acq sfr
     local sfrscr=self:getSkillArgByName(clsid,"OverHeatScp")
     globalself=self
     if(sfrscr==nil or sfrscr=="" or sfrscr=="nan")then
          return GetSkill(self,clsid,level).SklUseOverHeat
     end
     return _G[sfrscr](GetSkill(self,clsid,level))
end