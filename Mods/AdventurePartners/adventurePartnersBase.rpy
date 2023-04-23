# Note: Because they didn't create the databases in an "init" statement, I'm not sure if this will run into problems. If it does, change it to a label and have the script (hopefully) call it after it calls "loadDatabase".

# init -1 python in adventurePartner:
default PartnerDatabase = []
default PartnerDatabaseVersion = 1
default adventurePartner = AdventurePartner()
default canPartner = True # Can partner at all?
default partnerName = "" # Stores partner name for reloading later.
default persistant.pestering = False
default persistant.duplicateEnemies = True
default persistant.genericDamageMult = 0.75
default persistant.uniqueDamageMult = 1.5

# Can partner with specific girls?
default canPartnerAiko = False
default canPartnerAmy = False
default canPartnerAncilla = False
default canPartnerBelle = False
default canPartnerBeris = False
default canPartnerCamilla = False
default canPartnerCatherine = False
default canPartnerCeris = False
default canPartnerFeng = False
default canPartnerGalvi = False
default canPartnerGren = False
default canPartnerHeather = False
default canPartnerHimika = False
default canPartnerIabel = False
default canPartnerJennifer = False
default canPartnerJora = False
default canPartnerKotone = False
default canPartnerKyra = False
default canPartnerLumiren = False
default canPartnerMara = False
default canPartnerMika = False
default canPartnerMinoni = False
default canPartnerMizuko = False
default canPartnerNara = False
default canPartnerNicci = False
default canPartnerNova = False
default canPartnerRika = False
default canPartnerRosaura = False
default canPartnerSalarisi = False
default canPartnerSelena = False
default canPartnerShizu = False
default canPartnerSophia = False
default canPartnerStella = False
default canPartnerTabitha = False
default canPartnerTrisha = False
default canPartnerUshris = False
default canPartnerVenefica = False
default canPartnerVili = False
default canPartnerVoltlin = False
default canPartnerAmber = False
default canPartnerElena = False
default canPartnerElly = False
default canPartnerLillian = False
default canPartnerVivian = False





init 1 python:
  # I don't know if this function exists somewhere else, but I wanted it, so I'm including it here.
  def getMonsterByID(baseMonsterID = "Not, but my shadow"):
    # Get baseMonster from database by "IDname".
    for monster in MonsterDatabase:
      if(monster.IDname == baseMonsterID):
        # self.baseID = baseMonsterID # I'm setting this one here, because I don't want it to change.
        return monster
        # setData(monster)
        # break # No point in looking through others if we've found it.
  def getPartnerByID(partnerID = "Not, but my shadow"):
    for partner in PartnerDatabase:
      if(partnerID in partner.IDname):
        return partner
  
  def loadPartnerDatabase():
    global PartnerDatabase
    # =============================
    # ===== Database Updater ======
    # =============================
    renpy.log("Info: Loading adventure partner database.")
    PartnerDatabase = []
    for filename in dynamic_loader(".*/Partners/.*"):
    # for filename in dynamic_loader(".*/Mods/*/Partners/*.json"): # Hopefully, this will load any JSON files from any mod, not just my own.
      
      # Load the data from the file.
      # print filename # Debug purposes only.
      content = renpy.file(filename).read().decode("utf-8")
      try:
        # renpy.log(filename + " will be parsed for adventure partners.")
        currentData = json.loads(content)
      except:
        # renpy.log("Exception while loading partner file.")
        PrintException(content)
        renpy.log("Debug: Current content: " + content)
      
      
      
      # Parse the data.
      IDname = []
      if("IDname" in currentData):
        for id in currentData["IDname"]:
          IDname.append(id)
      idCount = len(IDname)
      
      if("baseID" in currentData):
        baseID = currentData["baseID"]
      elif(idCount == 0):
        renpy.log("Debug: No valid ID found for partner. Skipping " + filename + ".")
        break
      else:
        baseID = IDname[0]
      
      advancementPerk = []
      if("advancementPerk" in currentData):
        for perk in currentData["advancementPerk"]:
          if(len(perk) > 0):
            renpy.log("Advancement perk found while loading partner: "+str(perk))
            advancementPerk.append(perk)
      perkCount = len(advancementPerk)
            
      pesterScenes = []
      if("pesterScenes" in currentData):
        for each in currentData["pesterScenes"]:
          blankScene = LossScene()
          blankScene.NameOfScene = each["NameOfScene"]
          blankScene.move = each["move"]
          blankScene.stance = each["stance"]
          blankScene.includes = each["includes"]
          blankScene.theScene = each["theScene"]
          blankScene.picture = each["picture"]
          if validateJsons == True:
            validator.checkEventText(currentData["IDname"], blankScene, fileName)
          if additionLocation != None:
            if loadingDatabaseType == 0:
              MonsterDatabase[additionLocation].lossScenes.append(blankScene)
          else:
            pesterScenes.append(blankScene)
      
      if("flipImage" in currentData): # These image values should really be added to the monsters database, so that they can change when the partner level's up to a monster with a new image, but I don't want to modify that database, as it's likely to keep changing as the developers work on the game.
        flipImage = currentData["flipImage"]
      else:
        flipImage = []
      
      cropImage = []
      if("cropImage" in currentData):
        for value in currentData["cropImage"]:
          cropImage.append(int(value))
      else:
        cropImage = []
      
      positionImage = []
      if("positionImage" in currentData):
        for value in currentData["positionImage"]:
          positionImage.append(int(value))
      else:
        positionImage = [0,0]
      
      if("tooltipDesc" in currentData):
        tooltipDesc = "" + currentData["tooltipDesc"]
      
      casualPoses = []
      combatPoses = []
      if("casualPoses" in currentData):
        casualPoses = currentData["casualPoses"]
      if("combatPoses" in currentData):
        combatPoses = currentData["combatPoses"]
      
      # renpy.log("Debug: idCount " + str(idCount) + ", perkCount " + str(perkCount) + ".")
      # Remove some of the most obvious errors.
      if(perkCount > idCount): # Some error checking before we add them to the database.
        # If they have more perks listed than monster ID's, pop off the extras.
        i = perkCount - idCount
        while(i > 0):
          advancementPerk.pop()
          i -= 1
        perkCount = len(advancementPerk)
      elif(idCount > perkCount):
        if(perkCount == 0 or advancementPerk[0] != ""): # If the first one is blank or missing, add it.
          advancementPerk.insert(0,"") # Add a blank requirement if it was omitted.
          perkCount = len(advancementPerk)
        i = idCount - perkCount
        while(i > 0): # Then, get rid of any that remain unmatched.
          IDname.pop()
          i -= 1
        idCount = len(IDname)
      # There is an edge case where the creator gives multiple id's the "" requirement, in which case, it will advance them past the earlier ones, but if someone is doing that, it's their problem to deal with!
      # renpy.log("Debug: idCount " + str(idCount) + ", perkCount " + str(perkCount) + ".")
      
      # Save the new partner to the database.
      # PartnerDatabase.append((baseID, IDname, advancementPerk, pesterScenes, flipImage, cropImage, positionImage)) # Old tuple way; replaced by object way.
      
      renpy.log("Info: Processing \"" + IDname[0] + "\" into partner database.")
      i = 0
      while(i < idCount):
        monster = getMonsterByID(IDname[i])
        partner = getPartnerByID(IDname[i])
        # renpy.log("Debug: Monter " + str(monster) + ", Partner " + str(partner) + ".")
        if(partner is None): # New data to be added.
          # if(loadingDatabaseType == 0): # Initial Load.
          # elif(loadingDatabaseType == 1): # Load from saved game.
            blankPartner = AdventurePartner() # Create the object
            
            # Set the data that is shared with the monster.
            blankPartner.setData(Monster(
              monster.stats,
              monster.moneyDropped,
              monster.name,
              monster.IDname,
              monster.species,
              monster.gender,
              monster.description,
              monster.encyclopedia,
              monster.tags,
              monster.skillList,
              monster.perks,
              monster.lossScenes,
              monster.victoryScenes,
              monster.combatDialogue,
              monster.BodySensitivity,
              monster.ItemDropList,
              monster.resistancesStatusEffects,
              monster.requires,
              monster.requiresEvent,
              monster.generic,
              monster.FetishList,
              monster.ImageSets,
              monster.statusEffects,
              monster.lowHealthMark,
              monster.combatStance,
              monster.CardType
            ))
            
            # Set the data that is unique to partners.
            blankPartner.baseID = baseID
            blankPartner.advancementPerk = advancementPerk
            blankPartner.pesterScenes = pesterScenes
            blankPartner.flipImage = flipImage
            blankPartner.cropImage = cropImage
            blankPartner.positionImage = positionImage
            blankPartner.tooltipDesc = tooltipDesc
            blankPartner.casualPoses = casualPoses
            blankPartner.combatPoses = combatPoses
            
            # Copy it into the database.
            PartnerDatabase.append(copy.deepcopy(blankPartner)) # You have to do this so that it does an actual copy of the object and not just the pointer.
            # renpy.log("Debug: " + IDname[i] + " partner data created.")
        else: # Updated data for existing entry.
          # partner.advancementPerk = advancementPerk[i] # To-Do: Find out why this yields "AttributeError: 'int' object has no attribute 'advancementPerk'"!!!!
          partner.pesterScenes = pesterScenes
          partner.flipImage = flipImage
          partner.cropImage = cropImage
          partner.positionImage = positionImage
          partner.casualPoses = casualPoses
          partner.combatPoses = combatPoses
          # renpy.log("Debug: " + IDname[i] + " partner data modified.")
        i += 1
      # End while-loop
    renpy.log("Info: Partner database loaded.")
  
  def reloadPartner():
    global PartnerDatabase, PartnerDatabaseVersion, adventurePartner
    currentDatabaseVersion = 1
    
    # Check for database version update.
    try:
      PartnerDatabaseVersion
      PartnerDatabase.casualPoses
    except:
      PartnerDatabaseVersion = 0
    
    if(PartnerDatabaseVersion < currentDatabaseVersion):
      renpy.log("Warning: Partner database is out of date. Now updating.")
      adventurePartner = AdventurePartner()
      PartnerDatabase = []
      loadPartnerDatabase()
      PartnerDatabaseVersion = currentDatabaseVersion
    
    # Make player not-generic
    player.generic = False
    
    # Reload Partner
    try:    adventurePartner
    except:
      # renpy.log("Cannot reload adventure partner \""+partnerName+"\".")
      adventurePartner
      return False
    else:
      return adventurePartner.setDataByID(partnerName)
  
  # Options Menu Functions
  def toggleDupEnemies():
    global persistant
    # renpy.log("Dup Enemies Before: " + str(persistant.duplicateEnemies))
    persistant.duplicateEnemies = not persistant.duplicateEnemies
    # renpy.log("Dup Enemies After: " + str(persistant.duplicateEnemies))
  def changeGenericDamageMult(input):
    global persistant
    # renpy.log("Input: "+str(input))
    persistant.genericDamageMult = float(int(input*20))/20 # Round down to next 5%
    # renpy.show_screen("Options")
  def changeUniqueDamageMult(input):
    global persistant
    persistant.uniqueDamageMult = float(int(input*20))/20
    # renpy.show_screen("Options")
  
  
  # =======================
  # ===== New Classes =====
  # =======================
  class AdventurePartner:
    # ----- Variables and Functions from Ren'Py's custom "Object" class -----
    # These are supposed to make the class easily serializable.
    __version__ = 0
    nosave = []
    after_setstate = None # None, to prevent this from being called when unnecessary.
    def __getstate__(self):
      rv = vars(self).copy()
      for f in self.nosave:
        if f in rv:
          del rv[f]
      rv["__version__"] = self.__version__
      return rv
    def __setstate__(self, new_dict):
      version = new_dict.pop("__version__", 0)
      self.__dict__.update(new_dict)
      if version != self.__version__:
        self.after_upgrade(version)  # type: ignore
      if self.after_setstate:
        self.after_setstate()
    
    # ----- Constructor -----
    # Note, if you want advancement to be possible, you'll need to create advanced monster JSON files and set their requirement to include "Always False", just in case a random monster thing is added at some point.
    def __init__(self):
      self.active = False # If the partner is selected and active at the current location. For instance, monstrous partners may not be allowed in town.
      self.folded = True # If the partner's UI screen is folded to the side.
      self.pesterCount = 0
      self.name = ""
      self.casualPoses = []
      self.combatPoses = []
    
    
    # ----- Special Member Functions -----
    def setData(self, baseMonster, basePartner = None):
      try: self.name != baseMonster.name # If they changed, reset pester counter.
      except:
        self.name = ""
      else:
        self.pesterCount = 0
      
      # Set partner stats from baseMonster.
      self.name                     = baseMonster.name
      self.IDname                   = baseMonster.IDname
      self.moneyDropped             = baseMonster.moneyDropped
      self.species                  = baseMonster.species
      self.gender                   = baseMonster.gender
      self.description              = baseMonster.description
      self.tags                     = baseMonster.tags
      self.skillList                = baseMonster.skillList
      self.perks                    = baseMonster.perks
      self.stats                    = baseMonster.stats
      self.lossScenes               = baseMonster.lossScenes
      self.victoryScenes            = baseMonster.victoryScenes
      self.combatDialogue           = baseMonster.combatDialogue
      self.statusEffects            = baseMonster.statusEffects # Was empty list [] or copy.deepcopy()
      self.lowHealthMark            = baseMonster.lowHealthMark
      self.BodySensitivity          = baseMonster.BodySensitivity
      self.FetishList               = baseMonster.FetishList
      self.ItemDropList             = baseMonster.ItemDropList
      self.combatStance             = baseMonster.combatStance
      self.CardType                 = baseMonster.CardType
      self.resistancesStatusEffects = baseMonster.resistancesStatusEffects
      self.requires                 = baseMonster.requires
      self.requiresEvent            = baseMonster.requiresEvent
      self.generic                  = baseMonster.generic
      self.encyclopedia             = baseMonster.encyclopedia
      self.restraintStruggle        = baseMonster.restraintStruggle
      self.restraintStruggleCharmed = baseMonster.restraintStruggleCharmed
      self.restraintEscaped         = baseMonster.restraintEscaped
      self.restraintEscapedFail     = baseMonster.restraintEscapedFail
      self.restrainer               = baseMonster.restrainer
      self.putInStance              = baseMonster.putInStance # Should be 0
      self.putInRestrain            = baseMonster.putInRestrain # Should be 0
      self.ImageSets                = baseMonster.ImageSets
      self.currentSet               = baseMonster.currentSet # Should be 0
      self.skippingAttack           = baseMonster.skippingAttack
      self.tooltipDesc              = baseMonster.description
      if(basePartner is None):
        self.baseID                 = self.IDname
        self.pesterScenes           = []
        self.flipImage              = True
        self.cropImage              = []    # [42,-33,458,658]
        self.positionImage          = [0,0] # [55,84]
        self.casualPoses            = []
        self.combatPoses            = []
      else:
        self.baseID                 = basePartner.baseID
        self.pesterScenes           = basePartner.pesterScenes
        self.flipImage              = basePartner.flipImage
        self.cropImage              = basePartner.cropImage
        self.positionImage          = basePartner.positionImage
        if(len(basePartner.tooltipDesc) > 0):
          self.tooltipDesc          = basePartner.tooltipDesc
        self.casualPoses            = basePartner.casualPoses
        self.combatPoses            = basePartner.combatPoses
      
      # self.advanceMonsterID         = "" # advanceMonsterID
      # self.advancementPerk          = "" # advancementPerk
      # self.baseID                   = basePartner[0] # This will get changed by the level advancer function if the partner gets leveled up.
      # self.pesterScenes             = basePartner.pesterScenes
      # self.pesterScenesCount        = len(basePartner[3])
      # self.flipImage                = basePartner[4]
      # self.cropImage                = basePartner[5] # [42,-33,458,658]
      # self.positionImage            = basePartner[6] # [55,84]
      
      # From Player
      # self.inventory = inventory
      # self.statPoints = statPoints
      # self.pastLevelUps = [[]]
      # self.pastLevelUpSens = []
      # self.lvlUps = lvlUps
      # self.resistancesStatusEffects = resistancesStatusEffects
      # self.BodySensitivity.Sex=100
      # self.BodySensitivity.Ass=100
      # self.BodySensitivity.Breasts=100
      # self.BodySensitivity.Mouth=100
      # self.BodySensitivity.Seduction=100
      # self.BodySensitivity.Magic=100
      # self.BodySensitivity.Pain=100
      # self.BodySensitivity.Holy=100
      # self.BodySensitivity.Unholy=100
      
      # Reset Stats
      self.stats.hp = 0 # self.stats.max_hp
      self.stats.ep = self.stats.max_ep
      self.stats.sp = self.stats.max_sp
      # renpy.retain_after_load() # This should make sure it gets stored, but I'm trying to make it inherit a revertable class instead.
      # return 1
    def setDataByID(self, monsterID):
      baseMonster = getMonsterByID(monsterID)
      basePartner = getPartnerByID(monsterID)
      # try: baseMonster
      # except:
      #   renpy.log("Debug: Monster is invalid; cannot set partner data.")
      # else:
      if(baseMonster is None):
        renpy.log("Debug: No monster data found for \"" + str(monsterID) + "\"; cannot set partner data.")
        return "Monster not found."
      elif(basePartner is None):
        renpy.log("Debug: No partner data found for \"" + str(monsterID) + "\"; cannot set partner data.")
        return "Partner not found."
      else:
        self.setData(baseMonster, basePartner)
        adventurePartner.startingPartnerImage()
        adventurePartner.advancePartnerLevel()
        renpy.hide_screen("AdventurePartnerMinimized")
        renpy.show_screen("AdventurePartnerScreen") # Could pass dissolve=False
        # canPartner = False
        renpy.log("Using monster \""+self.IDname+"\" as partner \""+self.name+"\" at level "+str(self.stats.lvl)+".")
        return "Partner found."
    def advancePartnerLevel(self, playerPerkList = []):
      global player
      # renpy.log("Checking partner \""+self.IDname+"\" for advancement.")
      partnerDisplay = copy.deepcopy(self.ImageSets)
      updateDisplay = False
      
      # Search database for manually leveled up version first.
      for partner in PartnerDatabase:
        # renpy.log("  Test Partner \""+partner.baseID+"\".")
        if(partner.baseID == self.baseID): # Look through the partners for ones with the same baseID.
          if(len(partner.advancementPerk) == 0):
            # renpy.log("  No advancement perk needed for partner \""+self.IDname+"\".")
            for monster in MonsterDatabase:
              if(partner.baseID in monster.IDname and self.IDname != monster.IDname):
                if(monster.stats.lvl <= player.stats.lvl):
                  # renpy.log("Using upgraded version \""+monster.IDname+"\" of this partner.")
                  self.setData(monster, partner)
                  updateDisplay = True
                # else:
                #   renpy.log("Not using upgraded version \""+monster.IDname+"\" of this partner.")
            else:
              continue # partner loop
            break # partner loop
          elif(len(partner.advancementPerk) == 1 and partner.advancementPerk[0] == ""):
            # renpy.log("  Blank advancement perk needed for partner \""+self.IDname+"\".")
            for monster in MonsterDatabase:
              if(partner.baseID in monster.IDname and self.IDname != monster.IDname):
                if(monster.stats.lvl <= player.stats.lvl):
                  # renpy.log("Using upgraded version \""+monster.IDname+"\" of this partner.")
                  self.setData(monster, partner)
                  updateDisplay = True
                # else:
                #   renpy.log("Not using upgraded version \""+monster.IDname+"\" of this partner.")
            else:
              continue # partner loop
            break # partner loop
          else:
            # renpy.log("  Advancement perk(s) are needed for partner \""+self.IDname+"\".")
            for playerPerk in playerPerkList:
              if(partner.advancementPerk in playerPerk): # If the player has the required perk, look up the monster in the database.
                for monster in MonsterDatabase:
                  if(partner.baseID in monster.IDname and self.IDname != monster.IDname): # and self.stats.lvl > monster.stats.lvl): # I'm cutting this last part, in case someone wants to give a perk that decreases a monster's level, for some reason. Beware that this means that monsters should be listed in the partner JSON in ascending order of power (so the last valid one is kept).
                    if(monster.stats.lvl <= player.stats.lvl):
                      # renpy.log("Using upgraded version \""+monster.IDname+"\" of this partner.")
                      # self = setData(monster)
                      self.setData(monster, partner)
                      # self.advancePartnerLevel(playerPerkList) # Recursively call this, in case it needs to level up more than once. Be careful about this as each one of these has three loops and it could be a resource hog!
                      # return True # While the following else-continue-break should work, I don't need it.
                      updateDisplay = True
                    # else:
                    #   renpy.log("Not using upgraded version \""+monster.IDname+"\" of this partner.")
                    # break # monster loop; No point in looking through others if we've found it.
                # else:     # All these else-continue-break lines accomplish this.
                #   continue
                # break
            return False
      if(updateDisplay):
        adventurePartner.startingPartnerImage()
        # could go through "partnerDisplay" and turn display to True in self.ImageSets for everything that's true in the saved version.
      
      # Improve stats to cath up to the player's level.
      # renpy.log("Upgrading partner \""+self.IDname+"\".")
      statPriority = [
        ["Power",self.stats.Power],
        ["Tech", self.stats.Tech],
        ["Int", self.stats.Int],
        ["Allure", self.stats.Allure],
        ["Willpower", self.stats.Willpower],
        ["Luck", self.stats.Luck],
        ["max_hp", self.stats.max_hp],
        ["max_ep", self.stats.max_ep],
        ["max_sp", self.stats.max_sp]
      ]
      statPriority.sort(reverse=True, key=lambda a: a[1])
      # statKeys = ["max_hp","max_ep","max_sp","Power","Tech","Int","Willpower","Allure","Luck"] # "hp","ep","sp"
      
      baseSP = self.stats.max_true_sp
      while(self.stats.lvl < player.stats.lvl):
        self.stats.lvl += 1
        statPoints = 3
        statSelected = 0
        # Increase SP every tenth level, max three times.
        if(self.stats.lvl % 10 == 0 and self.stats.max_true_sp - baseSP < 3):
          self.stats.sp += 1
          self.stats.max_sp += 1
          self.stats.max_true_sp += 1
          statPoints -= 1
        # Always give more hp.
        statPoints -= 1
        self.stats.max_hp += 10
        self.stats.max_true_hp += 10
        # Sometimes give more ep.
        if(self.stats.max_ep < 50 or self.stats.max_ep < 2 * self.stats.lvl):
          statPoints -= 1
          self.stats.max_ep += 10
          self.stats.max_true_ep += 10
        self.stats.ep = self.stats.max_ep # Refill ep on level up.
        
        # Spend the rest of the stat points on attributes.
        while(statPoints > 0):
          statSelected += renpy.random.choice([0,0,1]) # Random chance that a lower priority stat gets improved.
          if(statPriority[statSelected][0] == "Power"):
            statPoints -= 1
            self.stats.Power += 1
          elif(statPriority[statSelected][0] == "Tech"):
            statPoints -= 1
            self.stats.Tech += 1
          elif(statPriority[statSelected][0] == "Int"):
            statPoints -= 1
            self.stats.Int += 1
          elif(statPriority[statSelected][0] == "Allure"):
            statPoints -= 1
            self.stats.Allure += 1
          elif(statPriority[statSelected][0] == "Willpower"):
            statPoints -= 1
            self.stats.Willpower += 1
          elif(statPriority[statSelected][0] == "Luck"):
            statPoints -= 1
            self.stats.Luck += 1
          statSelected += 1
      return False
    def pester(self): # erroneousArguments = 0
      renpy.call_in_new_context("pesterPartner")
      # if(self.pesterCount < self.pesterScenesCount):
        # pass
      # elif(self.pesterScenesCount > 0):
        # pass # dialogue[self.pesterCount % self.pesterScenesCount]
      # else:
        # if(self.gender == "female"):
          # renpy.say(None, "She doesn't seem interested in talking right now.")
        # elif(self.gender == "male"):
          # renpy.say(None, "He doesn't seem interested in talking right now.")
        # else:
          # renpy.say(None, "They don't seem interested in talking right now.")
      # self.pesterCount += int(_return)
      # Hide partner screen if they're gone.
      if(adventurePartner.name == ""):
        renpy.hide_screen("AdventurePartnerScreen")
        renpy.show_screen("AdventurePartnerMinimized")
      # return False
    
    
    # ----- Standard functions for monster characters -----
    def giveStance(self, name, target, skill=Skill(),  holdoverDura=0):
      if name != "":
        # Remove any stances that are "none".
        i = 0
        for each in self.combatStance:
          if each.Stance == "None":
            del self.combatStance[i]
          i+=1
        
        # Check for stance continuation.
        durability = getStanceHoldRoll(self)
        if skill.name != "blank":
          fetishMod = 0
          for fetishTag in skill.fetishTags:
            for fetishList in target.FetishList:
              checkTag = fetishTag
              if(checkTag == "Penetration"):
                for stanceCheck in self.combatStance:
                  if stanceCheck.Stance == "Sex":
                    checkTag = "Sex"
                  elif stanceCheck.Stance == "Anal":
                    checkTag = "Ass"
              if(checkTag == fetishList.name):
                fetishMod += fetishList.Level
          durability += durability*(fetishMod*0.005) + (fetishMod*0.1)
        self.combatStance.append(CombatStance(name, durability+holdoverDura))
    def clearStance(self):
      numberOStance = len(self.combatStance)
      i = 0
      while(i < numberOStance):
        del self.combatStance[0]
        i += 1
      self.combatStance.append(CombatStance("None"))
    def getStanceDurability(self, theName):
      i = 0
      durability = 0
      stanceRemoved = 0
      for x in self.combatStance:
       if (x.Stance == theName and stanceRemoved == 0) or theName == "All":
        durability = self.combatStance[i].potency
        stanceRemoved = 1
       i += 1
      return durability
    def removeStanceByName(self, theName):
      i = 0
      for x in self.combatStance:
        if x.Stance == theName  or theName == "All":
          del self.combatStance[i]
        i += 1
      if len(self.combatStance) <= 0:
        self.combatStance.append(CombatStance("None"))
    def giveOrTakePerk(self, perkName, GiveOrTake, duration= -2):
      if GiveOrTake == 1:
          # Is this broken into two lines simply because they used multiple names, rather than standardizing them?
          fetchPerk = getFromName(perkName, PerkDatabase)
          aquiredPerk = PerkDatabase[fetchPerk]
      else:
          fetchPerk = getFromName(perkName, self.perks)
          aquiredPerk = self.perks[fetchPerk]

      p = 0
      while  p < len(aquiredPerk.PerkType):
        # Note: The original code had these as seperate if-statements, but they should be elif, because you'll never have the name be equal to two different things.
        if aquiredPerk.PerkType[p] == "GainSpirit" or aquiredPerk.PerkType[p] == "Gain Spirit":
            self.stats.max_sp += aquiredPerk.EffectPower[p] * GiveOrTake
            self.stats.sp += aquiredPerk.EffectPower[p] * GiveOrTake
            self.stats.max_true_sp = self.max_sp
        # Health perks
        elif aquiredPerk.PerkType[p] == "GainEnergy" or aquiredPerk.PerkType[p] == "Gain Energy":
            self.stats.max_ep += aquiredPerk.EffectPower[p] * GiveOrTake
            self.stats.max_true_ep = self.stats.max_ep
        elif aquiredPerk.PerkType[p] == "GainArousal" or aquiredPerk.PerkType[p] == "Gain Arousal":
            self.stats.max_hp += aquiredPerk.EffectPower[p] * GiveOrTake
            self.stats.max_true_hp = self.stats.max_hp
        # Stat perks
        elif aquiredPerk.PerkType[p] == "Power":
            self.stats.Power += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "Technique":
            self.stats.Tech += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "Intelligence":
            self.stats.Int += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "Allure":
            self.stats.Allure += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "Willpower":
            self.stats.Willpower += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "Luck":
            self.stats.Luck += aquiredPerk.EffectPower[p] * GiveOrTake
        # Resistance perks
        elif aquiredPerk.PerkType[p] == "StunRes" or aquiredPerk.PerkType[p] == "Stun Res":
            self.resistancesStatusEffects.Stun += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "CharmRes" or aquiredPerk.PerkType[p] == "CharmRes":
            self.resistancesStatusEffects.Charm += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "AphrodisiacRes" or aquiredPerk.PerkType[p] == "Aphrodisiac Res":
            self.resistancesStatusEffects.Aphrodisiac += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "RestraintsRes" or aquiredPerk.PerkType[p] == "Restraints Res":
            self.resistancesStatusEffects.Restraints += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "SleepRes" or aquiredPerk.PerkType[p] == "Sleep Res":
            self.resistancesStatusEffects.Sleep += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "TranceRes" or aquiredPerk.PerkType[p] == "Trance Res":
            self.resistancesStatusEffects.Trance += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "ParalysisRes" or aquiredPerk.PerkType[p] == "Paralysis Res":
            self.resistancesStatusEffects.Paralysis += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "DebuffRes" or aquiredPerk.PerkType[p] == "Debuff Res":
            self.resistancesStatusEffects.Debuff += aquiredPerk.EffectPower[p] * GiveOrTake
        # Sensitivity perks
        elif aquiredPerk.PerkType[p] == "SexSensitivity" or aquiredPerk.PerkType[p] == "Sex Sensitivity":
            self.BodySensitivity.Sex += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "AssSensitivity" or aquiredPerk.PerkType[p] == "Ass Sensitivity":
            self.BodySensitivity.Ass += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "BreastsSensitivity" or aquiredPerk.PerkType[p] == "Breasts Sensitivity":
            self.BodySensitivity.Breasts += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "MouthSensitivity" or aquiredPerk.PerkType[p] == "Mouth Sensitivity":
            self.BodySensitivity.Mouth += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "SeductionSensitivity" or aquiredPerk.PerkType[p] == "Seduction Sensitivity":
            self.BodySensitivity.Seduction += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "MagicSensitivity" or aquiredPerk.PerkType[p] == "Magic Sensitivity":
            self.BodySensitivity.Magic += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "PainSensitivity" or aquiredPerk.PerkType[p] == "Pain Sensitivity":
            self.BodySensitivity.Pain += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "HolySensitivity" or aquiredPerk.PerkType[p] == "Holy Sensitivity":
            self.BodySensitivity.Holy += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "UnholySensitivity" or aquiredPerk.PerkType[p] == "Unholy Sensitivity":
            self.BodySensitivity.Unholy += aquiredPerk.EffectPower[p] * GiveOrTake
        elif aquiredPerk.PerkType[p] == "IncreaseFetish" or aquiredPerk.PerkType[p] == "DecreaseFetish" or aquiredPerk.PerkType[p] == "Increase Fetish" or aquiredPerk.PerkType[p] == "Decrease Fetish": # This is why we standardize terminology!
          resTarget = aquiredPerk.EffectPower[p]
          parsed = aquiredPerk.EffectPower[p].partition("|/|")
          baseFetish = self.getFetish(parsed[0])
          
          if parsed[2] == "":
              multi = 1
          else:
              multi = int(parsed[2])
              
          if aquiredPerk.PerkType[p] == "IncreaseFetish" or aquiredPerk.PerkType[p] == "Increase Fetish":
              baseFetish += multi * GiveOrTake
          else:
              baseFetish -= multi * GiveOrTake
          self.setFetish(parsed[0], baseFetish)
        p += 1
      # End While Loop
      
      if GiveOrTake == 1:
        self.perks.append(copy.deepcopy(PerkDatabase[fetchPerk]))
        if duration != -2:
          self.perks[-1].duration = duration
      else:
        del self.perks[fetchPerk]
      
      # Red's Addition
      renpy.log("Perk Gained/Lossed; Reseting monsterEncounter to [].")
      monsterEncounter = [] # Hopefully this will fix a bug causing an infinite loop.
      return
    def getFetish(self, name):
      for each in self.FetishList:
        if each.name == name:
          return each.Level
      return 0
    def setFetish(self, name, number):
      L = 0
      for each in self.FetishList:
        if each.name == name:
          self.FetishList[L].Level = number
        L += 1
      return
    def fetishTotal(self):
      total = 0
      for each in self.FetishList:
        total += each.Level
      return total
    # ----- New Combat Functions for Partners -----
    def selectTarget(self, ally, enemies):
      # global player, enemies
      moves = []
      struggle = getStanceStruggleRoll(self)
      
      # Unconscious -> fade away.
      if(self.stats.sp < 1):
        renpy.say(None, self.name +" fades away.")
        partnerName = ""
        adventurePartner = AdventurePartner()
        return [None, []]
      
      # Free Self
      negativeStances = []
      potency = 0
      if(len(self.combatStance) > 0 and self.combatStance[0].Stance != "None"):
        # Find negative stances
        for i in range(len(self.combatStance)):
          if(self.combatStance[i].potency > 0):
            negativeStances.append(i)
            potency += self.combatStance[i].potency
        
        # Struggle against negative stances
        struggle /= max(1, len(negativeStances))
        for i in range(len(negativeStances)):
          self.combatStance[i].potency -= struggle
          if(self.combatStance[i].potency <= 0):
            # Remove stance from enemy first
            for enemy in enemies:
              for es in range(len(enemy.combatStance)):
                if(enemy.combatStance[es].Stance == self.combatStance[i].Stance and enemy.combatStance[es].WithWho == self.name):
                  enemy.combatStance.pop(es)
            # Remove stance from self
            self.combatStance.pop(i)
            if(len(self.combatStance) == 0): # Have to give a "None-stance" for some reason.
              self.combatStance = [{}]
              self.combatStance[0].Stance = "None"
              self.combatStance[0].WithWho = "None"
              self.combatStance[0].potency = 0
              renpy.say(None, self.name +" broke free.")
      
      # Stunned and Can't Act
      # if(self.statusEffects.stunned.duration +
      #    self.statusEffects.sleep.duration +
      #    self.statusEffects.surrender.duration +
      #    self.statusEffects.restrained.duration +
      #    self.statusEffects.trance.duration +
      #    self.statusEffects.paralysis.duration +
      #    self.statusEffects.fascinated.duration > 0):
      #   renpy.say(None, self.name +" is unable to act.")
      #   return [None, []]
      
      # Free Player
      negativeStances = []
      potency = 0
      if(len(ally.combatStance) > 0 and ally.combatStance[0].Stance != "None"):
        # Find negative stances
        for i in range(len(ally.combatStance)):
          if(ally.combatStance[i].potency > 0):
            negativeStances.append(i)
            potency += ally.combatStance[i].potency
        
        # Struggle against negative stances
        struggle /= max(1, len(negativeStances))
        for i in range(len(negativeStances)):
          ally.combatStance[i].potency -= struggle
          if(ally.combatStance[i].potency <= 0):
            # Remove stance from enemy first
            for enemy in enemies:
              for es in range(len(enemy.combatStance)):
                if(enemy.combatStance[es].Stance == ally.combatStance[i].Stance and enemy.combatStance[es].WithWho == ally.name):
                  enemy.combatStance.pop(es)
            # Remove stance from ally
            ally.combatStance.pop(i)
            if(len(ally.combatStance) == 0): # Have to give a "None-stance" for some reason.
              ally.combatStance = [{}]
              ally.combatStance[0].Stance = "None"
              ally.combatStance[0].WithWho = "None"
              ally.combatStance[0].potency = 0
              renpy.say(None, self.name +" pulled you free.")
      
      # Find the different types of skills
      heals = []
      mana = []
      buffs = []
      debuffs = []
      attacks = []
      other = []
      buffableStats = ["bonus_hp","bonus_ep","Power","Tech","Int","Willpower","Allure","Luck"] # "hp","max_hp","ep","max_ep","sp","max_sp"
      for i in range(len(self.skillList)):
        if(self.skillList[i].skillType.lower() == "healing"):
          heals.append(i)
        elif(self.skillList[i].skillType.lower() == "healingep"):
          mana.append(i)
        # elif(self.skillList[i].statusEffect in ["Restrain","Sleep"]):
        #   stuns.append(i)
        elif("Buffs" in self.skillList[i].skillTags):
          buffs.append(i)
        elif("Afflictions" in self.skillList[i].skillTags):
          debuffs.append(i)
        elif(self.skillList[i].skillType.lower() == "attack"):
          attacks.append(i)
        else:
          other.append(i)
      
      # Heal Self
      for i in range(len(heals)):
        # Give a priority that is the fraction of health this will heal.
        effectiveHP = self.stats.max_hp * self.stats.sp
        priority = max(0, effectiveHP - max(0, self.stats.hp - self.skillList[heals[i]].minRange))
        if(self.stats.sp == 1): # Extra priority if last SP
          priority *= 1.5
        else:
          priority += self.stats.max_hp * (self.stats.sp - 1)
        moves.append({})
        moves[-1].index = heals[i]
        moves[-1].priority = priority/(self.stats.max_hp * self.stats.max_sp) 
        moves[-1].target = -1 # -1 = self, -2 = ally, -100: all allies, 0-99 = enemies index, 100 = all enemies
        renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ self.name +" with priority "+ str(moves[-1].priority) +".")
      
      # Mana Self
      for i in range(len(mana)):
        # Give a priority that is the fraction of health this will heal.
        priority = max(0, self.stats.ep - max(0, self.stats.ep - self.skillList[mana[i]].minRange))/self.stats.max_ep
        if(self.stats.ep == 0 and self.stats.max_ep > 0): # High priority if no mana left.
          priority = 0.999
        elif(self.stats.ep < self.stats.max_ep * 0.25): # Extra priority if low on mana.
          priority *= 1.5
        elif(self.stats.ep > self.stats.max_ep * 0.75): # Low priority if already high mana.
          priority *= 0.1
        moves.append({})
        moves[-1].index = mana[i]
        moves[-1].priority = priority
        moves[-1].target = -1 # -1 = self, -2 = ally, -100: all allies, 0-99 = enemies index, 100 = all enemies
        renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ self.name +" with priority "+ str(moves[-1].priority) +".")
        
      # Heal Player
      for i in range(len(heals)):
        # Give a priority that is the fraction of health this will heal.
        effectiveHP = ally.stats.max_hp * ally.stats.sp
        priority = max(0, effectiveHP - max(0, ally.stats.hp - ally.skillList[heals[i]].minRange))
        if(ally.stats.sp == 1): # Extra priority if last SP
          priority *= 1.5
        else:
          priority += ally.stats.max_hp * (ally.stats.sp - 1)
        moves.append({})
        moves[-1].index = heals[i]
        moves[-1].priority = priority/(ally.stats.max_hp * ally.stats.max_sp) 
        moves[-1].target = -2 # -1 = self, -2 = ally, -100: all allies, 0-99 = enemies index, 100 = all enemies
        renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ ally.name +" with priority "+ str(moves[-1].priority) +".")
      
      # Mana Player
      for i in range(len(mana)):
        # Give a priority that is the fraction of health this will heal.
        priority = max(0, ally.stats.ep - max(0, ally.stats.ep - ally.skillList[mana[i]].minRange))/ally.stats.max_ep
        if(ally.stats.ep == 0 and ally.stats.max_ep > 0): # High priority if no mana left.
          priority = 0.999
        elif(ally.stats.ep < ally.stats.max_ep * 0.25): # Extra priority if low on mana.
          priority *= 1.5
        elif(ally.stats.ep > ally.stats.max_ep * 0.75): # Low priority if already high mana.
          priority *= 0.1
        moves.append({})
        moves[-1].index = mana[i]
        moves[-1].priority = priority
        moves[-1].target = -2 # -1 = self, -2 = ally, -100: all allies, 0-99 = enemies index, 100 = all enemies
        renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ ally.name +" with priority "+ str(moves[-1].priority) +".")
      
      # Buff Player
      #   Get best stats to buff
      buffStat = [] # [[Stat Name, Stat Value]]
      statTotal = 0
      for i in range(len(buffableStats)):
        if(buffableStats[i] in ["bonus_hp","bonus_sp"]): # Don't value these as highly
          buffStat.append([buffableStats[i], ally.stats.getStat(buffableStats[i])/5])
          statTotal += ally.stats.getStat(buffableStats[i])/5
        else:
          buffStat.append([buffableStats[i], ally.stats.getStat(buffableStats[i])])
          statTotal += ally.stats.getStat(buffableStats[i])
      buffStat.sort(reverse=True, key=lambda a: a[1])
      
      #   Match the move to the stat and add it
      for i in range(len(buffs)):
        priority = 0
        for j in range(len(buffStat)):
          if(self.skillList[buffs[i]].statType == buffStat[j][0]):
            priority  = (self.skillList[buffs[i]].statusPotency + buffStat[j][1]) / statTotal # Buff effectiveness
            priority *= (self.skillList[buffs[i]].statusDuration -1)/6 # Buff duration
            # priority *= j / len(buffStat) # Buffed stat priority; I'm leaving this off because I think the "buff effectiveness" line above will be sufficient.
            moves.append({})
            moves[-1].index = buffs[i]
            moves[-1].priority = min(0.9, priority) # Priority capped at 90%.
            moves[-1].target = -2 # -1 = self, -2 = ally, -100: all allies, 0-99 = enemies index, 100 = all enemies
            renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ ally.name +" with priority "+ str(moves[-1].priority) +".")
      
      # Buff Self
      #   Get best stats to buff
      buffStat = [] # [[Stat Name, Stat Value]]
      statTotal = 0
      for i in range(len(buffableStats)):
        if(buffableStats[i] in ["bonus_hp","bonus_sp"]): # Don't value these as highly
          buffStat.append([buffableStats[i], self.stats.getStat(buffableStats[i])/5])
          statTotal += self.stats.getStat(buffableStats[i])/5
        else:
          buffStat.append([buffableStats[i], self.stats.getStat(buffableStats[i])])
          statTotal += self.stats.getStat(buffableStats[i])
      buffStat.sort(reverse=True, key=lambda a: a[1])
      
      #   Match the move to the stat and add it
      for i in range(len(buffs)):
        priority = 0
        for j in range(len(buffStat)):
          if(self.skillList[buffs[i]].statType == buffStat[j][0]):
            priority  = (self.skillList[buffs[i]].statusPotency + buffStat[j][1]) / statTotal # Buff effectiveness
            priority *= (self.skillList[buffs[i]].statusDuration -1)/6 # Buff duration
            # priority *= j / len(buffStat) # Buffed stat priority; I'm leaving this off because I think the "buff effectiveness" line above will be sufficient.
            moves.append({})
            moves[-1].index = buffs[i]
            moves[-1].priority = min(0.9, priority) # Priority capped at 90%.
            moves[-1].target = -2 # -1 = self, -2 = self, -100: all allies, 0-99 = enemies index, 100 = all enemies
            renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ self.name +" with priority "+ str(moves[-1].priority) +".")
      
      # Debuff Enemy
      for en in range(len(enemies)):
        debuffStat = [] # [[Stat Name, Stat Value]]
        statTotal = 0
        resist = ""
        for i in range(len(buffableStats)):
          debuffStat.append([buffableStats[i], enemies[en].stats.getStat(buffableStats[i])])
          statTotal += enemies[en].stats.getStat(buffableStats[i])
        debuffStat.sort(reverse=True, key=lambda a: a[1])
        
        #   Match the move to the stat and add it
        for i in range(len(debuffs)):
          priority = 0
          for j in range(len(debuffStat)):
            if(self.skillList[debuffs[i]].statType == debuffStat[j][0]):
              priority  = (self.skillList[debuffs[i]].statusPotency + debuffStat[j][1]) / statTotal # Buff effectiveness
              # Reduce priority based on status chance and target resistance
              #   Possible status resistances: Charm, Trance, Paralysis, Debuff, Restraints, Stun, Sleep, Aphrodisiac
              if(self.skillList[debuffs[i]].statusEffect == "Aphrodisiac"):
                priority *= (self.skillList[debuffs[i]].statusChance - enemies[en].resistancesStatusEffects.Aphrodisiac) / 100
                priority *= (self.skillList[debuffs[i]].statusDuration -1)/6 # Buff duration
              elif(self.skillList[debuffs[i]].statusEffect in ["Power","Defense","Luck"]):
                priority *= (self.skillList[debuffs[i]].statusChance - enemies[en].resistancesStatusEffects.Debuff) / 100
                priority *= (self.skillList[debuffs[i]].statusDuration -1)/6 # Buff duration
              elif(self.skillList[debuffs[i]].statusEffect == "Charm"):
                priority *= (self.skillList[debuffs[i]].statusChance - enemies[en].resistancesStatusEffects.Charm) / 100
                priority *= (self.skillList[debuffs[i]].statusDuration -1)/6 # Buff duration
              elif(self.skillList[debuffs[i]].statusEffect == "Restrain"):
                priority *= (self.skillList[debuffs[i]].statusChance - enemies[en].resistancesStatusEffects.Restraints) / 100
                priority *= (self.skillList[debuffs[i]].statusDuration -1)/3 # Buff duration, lower because stunning an enemy is really good.
              elif(self.skillList[debuffs[i]].statusEffect =="Sleep"):
                priority *= (self.skillList[debuffs[i]].statusChance - enemies[en].resistancesStatusEffects.Sleep) / 100
                priority *= (self.skillList[debuffs[i]].statusDuration -1)/3 # Buff duration, lower because stunning an enemy is really good.
              else:
                priority *= self.skillList[debuffs[i]].statusChance / 100
              moves.append({})
              moves[-1].index = debuffs[i]
              moves[-1].priority = min(0.9, priority) # Priority capped at 90%.
              moves[-1].target = en # -1 = self, -2 = self, -100: all allies, 0-99 = enemies index, 100 = all enemies
              renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ enemies[en].name +" with priority "+ str(moves[-1].priority) +".")
      
      # Harm Enemy
      
      for i in range(len(attacks)):
        # renpy.log("Attacks: "+str(i)+"/"+str(len(attacks)))
        if(self.skillList[attacks[i]].targetType == "all"):
          priority = min(0.95, self.skillList[attacks[i]].minRange / enemies[0].stats.max_hp) # Priority capped at 95%.
          moves.append({})
          moves[-1].index = attacks[i]
          moves[-1].priority = min(0.95, priority) # Priority capped at 95%.
          moves[-1].target = 100 # -1 = self, -2 = ally, -100: all allies, 0-99 = enemies index, 100 = all enemies
          renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ enemies[en].name +" with priority "+ str(moves[-1].priority) +".")
        else:
          for en in range(len(enemies)):
            # renpy.log("Enemies: "+str(en)+"/"+str(len(enemies)))
            # Give a priority that is the fraction of health this will deal.
            effectiveHP = enemies[en].stats.max_hp * enemies[en].stats.sp
            priority = max(0, effectiveHP - max(0, enemies[en].stats.max_hp - self.skillList[attacks[i]].minRange))
            if(enemies[en].stats.sp == 1): # Extra priority if last SP
              priority *= 1.5
            else:
              priority += enemies[en].stats.max_hp * (enemies[en].stats.sp - 1)
            moves.append({})
            moves[-1].index = attacks[i]
            moves[-1].priority = min(0.95, priority/(enemies[en].stats.max_hp * enemies[en].stats.max_sp)) # Priority capped at 95%.
            moves[-1].target = en # -1 = self, -2 = ally, -100: all allies, 0-99 = enemies index, 100 = all enemies
            renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ enemies[en].name +" with priority "+ str(moves[-1].priority) +".")
      
      # Other Skill
      for i in range(len(other)):
        moves.append({})
        moves[-1].index = other[i]
        moves[-1].priority = 0.1
        moves[-1].target = -1 # -1 = self, -2 = ally, -100: all allies, 0-99 = enemies index, 100 = all enemies
        renpy.log(self.name +" considers "+ self.skillList[moves[-1].index].name +" on "+ ally.name +" with priority "+ str(moves[-1].priority) +".")
      
      # Viable Target Checks
      for i in range(len(moves)):
        # renpy.log("   moves["+str(i)+"].priority: "+str(moves[i].priority))
        # Adjust for AoE spells
        if(self.skillList[moves[i].index].targetType == "all"):
          if(moves[i].target < 0): # Player and partner
            moves[i].target = -100
            moves[i].priority *= 1.5 # Priority +50% for player and partner.
          else: # All enemies
            moves[i].target = 100
            moves[i].priority *= 0.5 + 0.5 * len(enemies) # Priority +50% for each additional enemy.
        # renpy.log("a  moves["+str(i)+"].priority: "+str(moves[i].priority))
        # Requires Stance
        try:
          self.skillList[moves[i].index].requiresStance[0]
        except:
          pass
        else:
          # renpy.log("Required: "+str(self.skillList[moves[i].index].requiresStance))
          if(self.skillList[moves[i].index].requiresStance not in ["", "None", "Any"]):
            missing = True
            for k in self.combatStance:
              # renpy.log("Has: "+str(k.Stance))
              if(k.Stance == self.skillList[moves[i].index].requiresStance):
                missing = False
                break # self stance
            if(missing):
              moves[i].priority = -100
        # renpy.log("b  moves["+str(i)+"].priority: "+str(moves[i].priority))
        # Requires Target Stance
        found = []
        try:
          self.skillList[moves[i].index].requiresTargetStance[0]
        except:
          pass
        else:
          # Red's Note: Does this need to check allies?
          # renpy.log("Required: "+str(self.skillList[moves[i].index].requiresStance))
          if(self.skillList[moves[i].index].requiresStance not in ["", "None", "Any"]):
            missing = True
            if(moves[i].target >= 0 and moves[i].target < 100):
              for k in enemies[moves[i].target].combatStance:
                if(k.Stance == self.skillList[moves[i].index].requiresStance):
                  missing = False
                  break # stance
              if(missing):
                moves[i].priority = -99
            elif(moves[i].target == 100):
              for en in enemies:
                for k in en.combatStance:
                  if(k.Stance == self.skillList[moves[i].index].requiresStance):
                    missing = False
                    break # stance
                else:
                  continue
                break # enemies
            elif(moves[i].target == -2):
              for k in player[moves[i].target].combatStance:
                if(k.Stance == self.skillList[moves[i].index].requiresStance):
                  missing = False
                  break # stance
              if(missing):
                moves[i].priority = -98
            elif(moves[i].target == -100):
              for k in self.combatStance: # Check Self
                if(k.Stance == self.skillList[moves[i].index].requiresStance):
                  missing = False
                  break # self stance
              if(not missing): # Check Player
                missing = True
                for k in player[moves[i].target].combatStance:
                  if(k.Stance == self.skillList[moves[i].index].requiresStance):                    
                    missing = False
                    break # stance
              if(missing):
                moves[i].priority = -97
        # renpy.log("c  moves["+str(i)+"].priority: "+str(moves[i].priority))
        # Requires Status
        found = []
        try:
          self.skillList[moves[i].index].requiresStatusEffect[0]
        except:
          pass
        else:
          if(self.skillList[moves[i].index].requiresStatusEffect not in ["", "None", "Any"]):
            missing = True
            effect = self.statusEffects[self.skillList[moves[i].index].requiresStatusEffect]
            if(str(type(effect)) == "<class 'store.StatusEffect'>"): # Single status
              if(effect.duration > 0 and effect.potency >= self.skillList[moves[i].index].requiresStatusPotency):
                missing = False
            elif(str(type(effect)) == "<class 'renpy.revertable.RevertableList'>"): # List of statuses
              for e in effect:
                if(e.duration > 0 and e.potency >= self.skillList[moves[i].index].requiresStatusPotency):
                  missing = False
                  break
            else:
              renpy.log("Error: Unknown effect type for partner \""+self.skillList[moves[i].index].requiresStatusEffect+"\".")
            if(missing):
              moves[i].priority = -102
        # renpy.log("d  moves["+str(i)+"].priority: "+str(moves[i].priority))
        # Unusable If Status
        found = []
        try:
          self.skillList[moves[i].index].unusableIfStatusEffect[0]
        except:
          pass
        else:
          for j in self.skillList[moves[i].index].unusableIfStatusEffect:
            # keys = self.statusEffects.__dict__.keys()
            try:
              len(self.statusEffects[j.lower()]) > 0
            except:
              break
            else:
              for k in self.statusEffects[j.lower()]:
                if(k.duration > 0):
                  moves[i].priority = -103
                  break # self status
              else:
                continue
              break # unusable if status
        # renpy.log("e  moves["+str(i)+"].priority: "+str(moves[i].priority))
        # Unusable If Stance
        found = []
        try:
          self.skillList[moves[i].index].unusableIfStance[0]
        except:
          pass
        else:
          for j in self.skillList[moves[i].index].unusableIfStance:
            for k in self.combatStance:
              if(j == k.Stance):
                moves[i].priority = -104
                break # self stance
            else:
              continue
            break # skill stance
        # renpy.log("f  moves["+str(i)+"].priority: "+str(moves[i].priority))
        # Unusable If Target Stance
        # unusableIfTarget
        found = []
        try:
          self.skillList[moves[i].index].unusableIfStance[0]
        except:
          pass
        else:
          for j in self.skillList[moves[i].index].unusableIfStance:
            if(moves[i].target == -2 or moves[i].target == -100): # Targeting ally or all friendlies
              for k in ally.combatStance:
                if(j == k.Stance):
                  moves[i].priority = -105
                  break # ally stance
              else:
                continue
              break # unusable if stance
            elif(moves[i].target == -1): # Targeting self; shouldn't happen, but it possible someone made a mistake in the JSON.
              for k in self.combatStance:
                if(j == k.Stance):
                  moves[i].priority = -105
                  break # self stance
              else:
                continue
              break # unusable if stance
            elif(moves[i].target >= 0): # Targeting enemy
              # renpy.log("Move target: "+str(moves[i].target))
              if(moves[i].target < 100):
                for k in enemies[moves[i].target].combatStance:
                  if(j == k.Stance):
                    moves[i].priority = -106
                    break # ally stance
                else:
                  continue
                break # unusable if stance
              else:
                for l in range(len(enemies)):
                  for k in enemies[l].combatStance:
                    if(j == k.Stance):
                      moves[i].priority = -107
                      break # ally stance
                  else:
                    continue
                  break # enemies
                else:
                  continue
                break # unusable if stance
      
      # renpy.log("g  moves["+str(i)+"].priority: "+str(moves[i].priority))
      # Multipliers
      for i in range(len(moves)):
        # Mana Efficiency
        if(self.skillList[moves[i].index].cost > 0):
          # renpy.log("Mana Efficiency Calc: ("+str(self.stats.ep)+"-"+str(self.skillList[moves[i].index].cost)+")/"+str(self.stats.max_ep)+".")
          mult = max(0.0, float(self.stats.ep - self.skillList[moves[i].index].cost)) / self.stats.max_ep
          # renpy.log("  Move["+str(i)+"] priority["+str(moves[i].priority)+"] multiplied by "+str(mult)+" due to mana efficiency.")
          moves[i].priority *= mult
        # Fetish & Sensitivity Multipliers
        mult = 1.0
        if(moves[i].target == 100): # Multiple enemies
          # Have to use a seperate multiplier or we'd get multiplicative results instead of additive.
          for tag in self.skillList[moves[i].index].fetishTags: # Fetishes
            for en in enemies:
              for fet in en.FetishList:
                if(tag == fet.name):
                  mult += fet.Level/100
                  break
          for tag in self.skillList[moves[i].index].skillTags: # Sensitivities
            for en in enemies:
              keys = en.BodySensitivity.__dict__.keys()
              for k in range(len(keys)):
                if(tag == keys[k]):
                  mult += en.BodySensitivity.getRes(keys[k])
                  break # Break key loop
              else:
                continue
              break # Break enemy loop
        elif(moves[i].target > -1): # Single enemy
          for tag in self.skillList[moves[i].index].fetishTags: # Fetishes
            for fet in enemies[moves[i].target].FetishList:
              if(tag == fet.name):
                mult *= (100 + fet.Level)/ 100
                break # Break fet loop
          for tag in self.skillList[moves[i].index].skillTags: # Sensitivities
            keys = enemies[moves[i].target].BodySensitivity.__dict__.keys()
            for k in range(len(keys)):
              if(tag == keys[k]):
                mult *= (100 + enemies[moves[i].target].BodySensitivity.getRes(keys[k]))/ 100
                break # Break key loop
        # renpy.log("  Move["+str(i)+"] priority["+str(moves[i].priority)+"] multiplied by "+str(mult)+" due to fetishes and sensitivities.")
        moves[i].priority *= mult
        
      
      # Sort moves by descending priority
      moves.sort(reverse=True, key=lambda(a): a.priority)
      
      # Add back in some randomness, trim list to a single move.
      for m in range(len(moves)):
        renpy.log("  Randomizer: Move "+str(m)+", "+self.skillList[moves[m].index].name+", Priority "+str(moves[m].priority)+".")
        if(moves[m].priority < moves[0].priority -0.2):
          if(m > 1):
            moves = [renpy.random.choice(moves[0:m-1])]
          else:
            moves = [moves[0]]
          break
      # rand = [0,0,0.1,0.2]
      # moves[0].priority += renpy.random.choice(rand)
      # if(len(moves) > 3):
      #   moves[3].priority += renpy.random.choice(rand)
      #   moves[2].priority += renpy.random.choice(rand)
      #   moves[1].priority += renpy.random.choice(rand)
      #   moves = moves[0:3]
      # elif(len(moves) > 2):
      #   moves[2].priority += renpy.random.choice(rand)
      #   moves[1].priority += renpy.random.choice(rand)
      #   moves = moves[0:2]
      # elif(len(moves) > 1):
      #   moves[1].priority += renpy.random.choice(rand)
      #   moves = moves[0:1]
      # Resort after randomness
      # moves.sort(reverse=True, key=lambda(a): a.priority)
      
      # Return [move, [target indecies]]
      if(moves[0].target == -1): # Target Self
        return [self.skillList[moves[0].index], [-1]]
      elif(moves[0].target == -2): # Target Ally
        return [self.skillList[moves[0].index], [-2]]
      elif(moves[0].target == -100): # Target all allies
        return [self.skillList[moves[0].index], [-1,-2]]
      elif(moves[0].target == 100): # Target all enemies
        return [self.skillList[moves[0].index], range(len(enemies))]
      else: # (moves[0].target > -1) # Target enemy
        return [self.skillList[moves[0].index], [moves[0].target]]
      
      # Return [move, [targets]]; OUTDATED
      if(moves[0].target == -1): # Target Self
        return [self.skillList[moves[0].index], [self]]
      elif(moves[0].target == -2): # Target Ally
        return [self.skillList[moves[0].index], [ally]]
      elif(moves[0].target == -100): # Target all allies
        return [self.skillList[moves[0].index], [self, ally]]
      elif(moves[0].target == 100): # Target all enemies
        return [self.skillList[moves[0].index], enemies]
      else: # (moves[0].target > -1) # Target enemy
        return [self.skillList[moves[0].index], [enemies[moves[0].target]]]
      
    # ----- Partner Image Functions -----
    def startingPartnerImage(self):
      imgName = None
      partName = None
      setName = None
      for setNum in range(len(self.ImageSets)):
        for partNum in range(len(self.ImageSets[setNum].ImageSet)):
          if(self.ImageSets[setNum].ImageSet[partNum].AlwaysOn > 0):
            self.ImageSets[setNum].display = True
            self.ImageSets[setNum].ImageSet[partNum].display = True
            self.ImageSets[setNum].ImageSet[partNum].Images[self.ImageSets[setNum].ImageSet[partNum].StartOn].display = True # Starting image if none is specified. Adding one to it, because there's some fucked up shit with the database that always adds a blank image listing.
      self.casualPartnerImage()
    def casualPartnerImage(self):
      if(len(self.casualPoses) > 0):
        pose = renpy.random.choice(self.casualPoses)
        for img in pose:
          if(len(img) > 2):
            self.showPartnerImage(img[0],img[1],img[2])
          elif(len(img) > 1):
            self.showPartnerImage(img[0],img[1])
          elif(len(img) > 0):
            self.showPartnerImage(img[0])
    def combatPartnerImage(self):
      if(len(self.casualPoses) > 0):
        pose = renpy.random.choice(self.combatPoses)
        for img in pose:
          if(len(img) > 2):
            self.showPartnerImage(img[0],img[1],img[2])
          elif(len(img) > 1):
            self.showPartnerImage(img[0],img[1])
          elif(len(img) > 0):
            self.showPartnerImage(img[0])
    def showPartnerImage(self, imgName, partName = None, setName = None):
      foundSet = None
      foundPart = None
      foundImg = None
      # Check if this should actually be a hide, instead.
      if(imgName == ""):
        return self.hidePartnerImage(imgName, partName, setName)
      # If we're showing an image, proceed.
      
      for setNum in range(len(self.ImageSets)):
        if(setName == None or setName == self.ImageSets[setNum].name):
          for partNum in range(len(self.ImageSets[setNum].ImageSet)):
            if(partName == None or partName == self.ImageSets[setNum].ImageSet[partNum].name):
              for imgNum in range(len(self.ImageSets[setNum].ImageSet[partNum].Images)):
                if(len(self.ImageSets[setNum].ImageSet[partNum].Images) == 1 or imgName == self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].name):
                  self.ImageSets[setNum].display = True
                  self.ImageSets[setNum].ImageSet[partNum].display = True
                  self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].display = True
                  foundSet = setNum
                  foundPart = partNum
                  foundImg = imgNum
                  break # The authors just kept naming everything "Base", so it matches the first thing every time.
              else: # Continue if the img loop wasn't broken.
                continue
              break # img loop was broken, break the outer.
          else: # Continue if the img loop wasn't broken.
            continue
          break # img loop was broken, break the outer.
        else:
          self.ImageSets[setNum].display = False
      # Turn off all other images on that part.
      if(foundImg is not None):
        for imgNum in range(len(self.ImageSets[foundSet].ImageSet[foundPart].Images)):
          if(imgNum != foundImg):
            self.ImageSets[foundSet].ImageSet[foundPart].Images[imgNum].display = False
        return self.ImageSets[foundSet].ImageSet[foundPart].Images[foundImg].file
      else:
        return False
    def hidePartnerImage(self, imgName, partName = None, setName = None):
      foundSet = None
      foundPart = None
      foundImg = None
      # renpy.log("Hiding: img("+imgName+"), part("+str(partName)+"), set("+str(setName)+").")
      for setNum in range(len(self.ImageSets)):
        if(setName is None or setName == self.ImageSets[setNum].Name):
          for partNum in range(len(self.ImageSets[setNum].ImageSet)):
            if(partName is None or partName == self.ImageSets[setNum].ImageSet[partNum].name):
              for imgNum in range(len(self.ImageSets[setNum].ImageSet[partNum].Images)):
                if(len(self.ImageSets[setNum].ImageSet[partNum].Images) == 1 or imgName == self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].name or len(imgName) == 0):
                  self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].display = False
                  foundSet = setNum
                  foundPart = partNum
                  foundImg = imgNum
                  break
              else: # Continue if the img loop wasn't broken.
                continue
              if(self.ImageSets[setNum].ImageSet[partNum].AlwaysOn > 0): # If always on, make sure to turn one back on.
                self.ImageSets[setNum].display = True
                self.ImageSets[setNum].ImageSet[partNum].display = True
                self.ImageSets[setNum].ImageSet[partNum].Images[self.ImageSets[setNum].ImageSet[partNum].StartOn].display = True
              break # img loop was broken, break the outer.
          else: # Continue if the img loop wasn't broken.
            continue
          break # img loop was broken, break the outer.
        else:
          self.ImageSets[setNum].display = False
      # Turn off all other images on that part.
      if(foundImg is not None):
        for imgNum in range(len(self.ImageSets[foundSet].ImageSet[foundPart].Images)):
          if(imgNum != foundImg):
            self.ImageSets[foundSet].ImageSet[foundPart].Images[imgNum].display = False
        return self.ImageSets[foundSet].ImageSet[foundPart].Images[foundImg].file
      else:
        return False
    def getPartnerImages(self):
      self.partnerImages = []
      for setNum in range(len(self.ImageSets)):
        try: self.ImageSets[setNum].display
        except: self.ImageSets[setNum].display = False
        if(self.ImageSets[setNum].display):
          for partNum in range(len(self.ImageSets[setNum].ImageSet)):
            try: self.ImageSets[setNum].ImageSet[partNum].display
            except: self.ImageSets[setNum].ImageSet[partNum].display = False
            if(self.ImageSets[setNum].ImageSet[partNum].display):
              for imgNum in range(len(self.ImageSets[setNum].ImageSet[partNum].Images)):
                try: self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].display
                except: self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].display = False
                if(self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].display):
                  self.partnerImages.append([
                    self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].file,
                    self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].setXalign,
                    self.ImageSets[setNum].ImageSet[partNum].Images[imgNum].setYalign
                  ])
                  break

  # ===== ===== ===== ===== ===== ===== ===== ===== ===== =====
  # End of the python.

init 2 python:
  loadPartnerDatabase() # Defined and immediately called. Not sure why this isn't working.
  if(reloadPartner not in config.after_load_callbacks):
    config.after_load_callbacks.append(reloadPartner)
  # try:
  #   adventurePartner
  # except:
  #   adventurePartner = AdventurePartner()
  # else:
  #   renpy.log("Adventure partner \""+adventurePartner.name+"\" already exists.")
  # adventurePartner.setData(getMonsterByID("Kyra"),getPartnerByID("Kyra"))
  # partnerName = renpy.random.choice(["Kyra","Minoni"])
  # if(getMonsterByID(partnerName) and getPartnerByID(partnerName)):
    # adventurePartner.setDataByID(partnerName)
    # Somehow, this was breaking things! It may be working now, but if statement is for safety. Was this running before she's in the database?

label reloadDatabases(): # Unused
  $ SkillsDatabase = []
  $ ItemDatabase = []
  $ MonsterDatabase = []
  $ PerkDatabase = []
  $ LocationDatabase = []
  $ EventDatabase = []
  $ AdventureDatabase = []
  $ LevelingPerkDatabase = []
  # $ PartnerDatabase = [] # Already done in the function.
  call loadDatabase()
  $ loadPartnerDatabase()
  return

# ===== Partner Labels =====
label pesterPartner():
  show screen AdventurePartnerScreen(False)
  $ passcheck = False
  # Don't allow stacking pestering.
  if(persistant.pestering):
    $ renpy.log("Stop pestering " + adventurePartner.name + "!")
    return False
  else:
    $ persistant.pestering = True
  
  # Look for scripted pester scenes.
  if(len(adventurePartner.pesterScenes) > 0):
    python:
      actorNames[0] = adventurePartner.name
      for loop in adventurePartner.pesterScenes:
        displayingScene = loop # Could look up in EventDatabase.theEvents, but it's easier to just put them in the partner files.
        lineOfScene = 0
        passcheck = SceneRequiresCheck()
        if(passcheck):
          adventurePartner.pesterCount += 1
          renpy.call("displayScene")
  
  # Otherwise, give a generic comment.
  if(passcheck):
    $ persistant.pestering = False
    return True
  elif(adventurePartner.gender == "female"):
    "She doesn't seem interested in talking right now."
  elif(adventurePartner.gender == "male"):
    "He doesn't seem interested in talking right now."
  else:
    "They don't seem interested in talking right now."
  $ persistant.pestering = False
  return False

