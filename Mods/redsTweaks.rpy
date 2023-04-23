default requirementChecks = [
  "HideOptionOnRequirementFail",
  "InverseRequirement",
  "ShuffleMenu",
  # "OverrideOption",
  "FinalOption",
  "EventJump",
  "RequiresMinimumProgressFromEvent", 
  "RequiresLessProgress",
  "RequiresLessProgressFromEvent",
  "RequiresChoice",
  "RequiresChoiceFromEvent",
  "RequiresTime",
  "RequiresStat",
  "RequiresFetishLevelEqualOrGreater",
  "RequiresFetishLevelEqualOrLess",
  "RequiresItem",
  "RequiresItemEquipped",
  "RequiresSkill",
  "RequiresPerk",
  "RequiresEnergy",
  "RequiresVirility",
  "RequiresProgressFromEvent",
  "RequiresVar",
  "RequiresVarValue"
]
default menuIndex = 0

# Replacement Choices Menu Screen
screen redsMenu(choices, caption="Blank Caption"):
  style_prefix "choice"
  modal True
  vbox:
    # style "menu"
    for choiceNum in range(len(choices)):
      $ renpy.log("Red's Menu Choice: " + str(choices[choiceNum]["text"]))
      if(choices[choiceNum]["page"] == menuIndex):
        # textbutton choices[choiceNum]["text"] style "choice_button" action [
        #   Function(renpy.log,"Button \""+ choices[choiceNum]["text"] +"\" pressed."),
        #   Hide("redsMenuPageButtons"),
        #   Hide("redsMenu"),
        #   Function(redsMenuSceneJump, choices[choiceNum]["jump"]),
        #   Return(choices[choiceNum]["jump"])
        # ]
        textbutton choices[choiceNum]["text"] style "choice_button" action Function(redsMenuSceneJump, choices[choiceNum]["jump"])
  if(caption):
    use say(None, caption)

# Left and Right Choices Menu Buttons
screen redsMenuPageButtons(pageCount):
  $ buttonIdleImgDown = "gui/Button_dec_idle_Jumbo.png"
  $ buttonHoverImgDown = "gui/Button_dec_hover_Jumbo.png"
  $ buttonIdleImgUp = "gui/Button_inc_idle_Jumbo.png"
  $ buttonHoverImgUp = "gui/Button_inc_hover_Jumbo.png"

  fixed:
    xalign LeftMenuScrollButtonX
    yalign 0.369
    imagebutton:
      idle buttonIdleImgDown
      hover buttonHoverImgDown
      xalign LeftMenuScrollButtonX
      yalign 0.369
      action menuPageIncrease(pageCount)
  fixed:
    xalign RightMenuScrollButtonX
    yalign 0.369
    imagebutton:
      idle buttonIdleImgUp
      hover buttonHoverImgUp
      xalign RightMenuScrollButtonX
      yalign 0.369
      action menuPageDecrease()

# Left and Right Choices Menu Button Functions
init python:
  def menuPageIncrease(pageCount):
    if(menuIndex < pageCount):
      ++menuIndex
  def menuPageDecrease():
    if(menuIndex > 0):
      --menuIndex
  def redsMenuSceneJump(name):
    global displayingScene, lineOfScene
    renpy.log("Python redsMenuSceneJump(\""+name+"\") called.")
    renpy.hide_screen("redsMenuPageButtons")
    renpy.hide_screen("redsMenu")
    # Red's Note: This code can only jump to scenes in the current event. I was using "DataLocation", but that variable isn't getting set for win/loss scenes, some of which have menus.
    for sc in range(len(EventDatabase[DataLocation].theEvents)):
      if(EventDatabase[DataLocation].theEvents[sc].NameOfScene == name):
        displayingScene = copy.deepcopy(EventDatabase[DataLocation].theEvents[sc])
        lineOfScene = 0 # Is this needed?
        renpy.log("  Jump target scene \""+ displayingScene.NameOfScene +"\" found.")
        return
    renpy.log("  Jump target scene \""+ name +"\" not found in \""+displayingScene.NameOfScene+"\".")
    lineOfScene = len(displayingScene.theScene)
    
    # Red's Note: This code would allow the user to jump to scenes in any event, not just the current one, but the scenes haven't been named uniquely, so I'm comparing both the current scene and the jump target. Hopefully this is enough to guarentee uniqueness.
    rightEvent = False
    # Check event database first.
    for ev in EventDatabase:
      # renpy.log("  Searching database event \""+ ev.name +"\" for current scene \""+ displayingScene.NameOfScene +"\".")
      # Find Current Scene
      for sc in ev.theEvents:
        if(sc.NameOfScene == displayingScene.NameOfScene):
          # renpy.log("  Current scene \""+ displayingScene.NameOfScene +"\" found.")
          rightEvent = True
          break # current sceen loop
      if(rightEvent):
        # renpy.log("  Searching database event \""+ ev.name +"\" for jump scene \""+ name +"\".")
        # Find Jump Scene
        for sc in ev.theEvents:
          if(sc.NameOfScene == name):
            displayingScene = copy.deepcopy(sc)
            # renpy.log("  Jump target scene \""+ displayingScene.NameOfScene +"\" found.")
            return
    
    # Check monster database second.
    for ev in MonsterDatabase:
      # renpy.log("  Searching database monster \""+ ev.name +"\" for current scene \""+ displayingScene.NameOfScene +"\".")
      # Find Current Scene
      if(ev.name == theLastAttacker.name):
        # renpy.log("  Searching database event \""+ ev.name +"\" for jump scene \""+ name +"\".")
        # Find Jump Scene
        for sc in ev.victoryScenes:
          if(sc.NameOfScene == name):
            displayingScene = copy.deepcopy(sc)
            # renpy.log("  Jump target scene \""+ displayingScene.NameOfScene +"\" found.")
            return
        for sc in ev.lossScenes:
          if(sc.NameOfScene == name):
            displayingScene = copy.deepcopy(sc)
            # renpy.log("  Jump target scene \""+ displayingScene.NameOfScene +"\" found.")
            return
    renpy.log("Error: No event found with jump target \""+name+"\".")
    return False
