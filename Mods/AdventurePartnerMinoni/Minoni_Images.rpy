default minoniPierced = False
default minoniThong = 0

layeredimage minoniBoobs:
  if(minoniPierced):
    "Mods/AdventurePartnerMinoni/Images/body_Minoni_Boobs_Pierced2.png"
  else:
    "Monsters/Minoni/body_Minoni_Boobs.png"
layeredimage minoniDress:
  if(minoniPierced):
    "Mods/AdventurePartnerMinoni/Images/body_Minoni_Clothing_Pierced.png"
  else:
    "Monsters/Minoni/body_Minoni_Clothing.png"
layeredimage minoniLower:
  if(minoniThong == 1):
    "Mods/AdventurePartnerMinoni/Images/lower_thong_tiger.png"
  elif(minoniThong == 2):
    "Mods/AdventurePartnerMinoni/Images/lower_thong_tigerWhite.png"

layeredimage minoniExpressionDemure:
  always "Mods/AdventurePartnerMinoni/Images/Eyes_Shy.png"
  always "Mods/AdventurePartnerMinoni/Images/Mouth_Serious.png"
  # always "Mods/AdventurePartnerMinoni/Images/Mouth_Base.png"
layeredimage minoniExpressionFlirty:
  always "Mods/AdventurePartnerMinoni/Images/Eyes_Serious.png"
  always "Mods/AdventurePartnerMinoni/Images/Mouth_Loving.png"

layeredimage minoni:
  # "Monsters/Minoni/.png"
  # "Mods/AdventurePartnerMinoni/Images/.png"
  group earR:
    attribute earRBase default "Mods/AdventurePartnerMinoni/Images/earR.png"
    attribute earRDroop        "Mods/AdventurePartnerMinoni/Images/earR_Droop.png"
  
  # Main Body
  always "Monsters/Minoni/body_Minoni_Base.png"
  
  group lower:
    attribute lowerBase default "minoniLower"
    attribute bare              Null()
    attribute tiger             "Mods/AdventurePartnerMinoni/Images/lower_thong_tiger.png"
    attribute whiteTiger        "Mods/AdventurePartnerMinoni/Images/lower_thong_tigerWhite.png"
  
  group blushes:
    attribute noBlush default Null()
    attribute blush           "Monsters/Minoni/Face_Minoni_Blush.png"
    attribute blushDeep       "Monsters/Minoni/Face_Minoni_Blush.png"
  
  group earL:
    attribute earLBase default "Mods/AdventurePartnerMinoni/Images/earR.png"
    attribute earLDroop        "Mods/AdventurePartnerMinoni/Images/earR_Droop.png"
  
  group armR:
    attribute armRBase default "Monsters/Minoni/ArmR_Base.png"
    attribute rWrestle         "Monsters/Minoni/ArmR_Wrestle.png"
  
  group dress:
    attribute nude          "minoniBoobs"
    attribute dress default "minoniDress"
    attribute piercedLeft   "Mods/AdventurePartnerMinoni/Images/body_Minoni_Boobs_PiercedLeft.png"
  
  group needleL:
    attribute needleLZero  "Mods/AdventurePartnerMinoni/Images/Minoni_NeedleLeft_0.png"
    attribute needleLOne   "Mods/AdventurePartnerMinoni/Images/Minoni_NeedleLeft_1.png"
    attribute needleLTwo   "Mods/AdventurePartnerMinoni/Images/Minoni_NeedleLeft_2.png"
    attribute needleLThree "Mods/AdventurePartnerMinoni/Images/Minoni_NeedleLeft_3.png"
  
  group needleR:
    attribute needleRZero  "Mods/AdventurePartnerMinoni/Images/Minoni_NeedleRight_0.png"
    attribute needleROne   "Mods/AdventurePartnerMinoni/Images/Minoni_NeedleRight_1.png"
    attribute needleRTwo   "Mods/AdventurePartnerMinoni/Images/Minoni_NeedleRight_2.png"
    attribute needleRThree "Mods/AdventurePartnerMinoni/Images/Minoni_NeedleRight_3.png"
  
  group armL:
    attribute armLBase default "Monsters/Minoni/ArmL_Base.png"
    attribute holdBook         "Monsters/Minoni/ArmL_BaseBook.png"
    attribute read             "Monsters/Minoni/ArmL_Read.png"
    attribute lWrestle         "Monsters/Minoni/ArmL_Wrestle.png"
  
  group hip:
    attribute hipEmpty default Null()
    attribute hipBook          "Monsters/Minoni/extra_minoni_book.png"
  
  group face:
    attribute base default "Monsters/Minoni/Expression_Minoni_Base.png"
    attribute angry        "Monsters/Minoni/Expression_Minoni_Angry.png"
    attribute Awawa        "Monsters/Minoni/Expression_Minoni_Awawa.png"
    attribute Cocky        "Monsters/Minoni/Expression_Minoni_Cocky.png"
    attribute Dominant     "Monsters/Minoni/Expression_Minoni_Dominant.png"
    attribute Embarrassed  "Monsters/Minoni/Expression_Minoni_Embarrassed.png"
    attribute Frustrated   "Monsters/Minoni/Expression_Minoni_Frustrated.png"
    attribute HappyClosed  "Monsters/Minoni/Expression_Minoni_HappyClosed.png"
    attribute Horny        "Monsters/Minoni/Expression_Minoni_Horny.png"
    attribute HornyDaze    "Monsters/Minoni/Expression_Minoni_HornyDaze.png"
    attribute Loving       "Monsters/Minoni/Expression_Minoni_Loving.png"
    attribute Pout         "Monsters/Minoni/Expression_Minoni_Pout.png"
    attribute Serious      "Monsters/Minoni/Expression_Minoni_Serious.png"
    attribute Shy          "Monsters/Minoni/Expression_Minoni_Shy.png"
    attribute Smile        "Monsters/Minoni/Expression_Minoni_Smile.png"
    attribute Sparkling    "Monsters/Minoni/Expression_Minoni_Sparkling.png"
    attribute Stumbling    "Monsters/Minoni/Expression_Minoni_Stumbling.png"
    attribute Stunned      "Monsters/Minoni/Expression_Minoni_Stunned.png"
    attribute Yummy        "Monsters/Minoni/Expression_Minoni_Dominant.png"
    attribute Demure       "minoniExpressionDemure"
    attribute Flirty       "minoniExpressionFlirty"
  
  group expressionCover:
    attribute noCover default Null()
    attribute expCover        "Monsters/Minoni/Face_Minoni_ExpressionCover.png"
  
  group sweat:
    attribute noSweat default Null()
    attribute nervousSweat    "Mods/AdventurePartnerMinoni/Images/sweat_Stumbling.png"

