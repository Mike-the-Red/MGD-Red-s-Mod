transform partnerSize67:
    zoom 0.67
transform partnerSize75:
  zoom 0.75
transform partnerSize80:
  zoom 0.8
transform partnerFlip:
  xzoom -1.0
transform crop(x,y,width,height):
  crop(x,y,width,height)
transform partnerPosition:
  xpos -45 # -55 or -43 @ 80%
  yalign 0.35
  zoom 0.8
transform opaque:
  alpha 1.0

screen movable_frame(posIn=(20,20)):
  drag:
    pos posIn
    transclude


screen AdventurePartnerScreen(dissolve = True): # partnerImage = "Mods/AdventurePartners/GUI/partner_kyra_normal_flipped.png"
  tag partner
  zorder 99
  frame id "partnerMainFrame":
    at partnerPosition
    # background "Mods/AdventurePartners/GUI/partnerBox.png"
    background "Mods/AdventurePartners/GUI/blankPixel.png"
    imagebutton:
      idle "Mods/AdventurePartners/GUI/partnerBox_192.png"
      focus_mask True
      action [Hide("AdventurePartnerScreen"), Show("AdventurePartnerMinimized"), Function(renpy.log,"Partner sidebar clicked.")]
      if(dissolve):
        at transform:
          alpha 0.0
          linear 0.25 alpha 1.0
    # fixed:
    #   xsize 458
    #   ysize 658
    #   add "Mods/AdventurePartners/GUI/partner_kyra_normal_flipped.png"
    #   xpos 0 # -3
    #   ypos 0 # -4
    
    use PartnerCard




screen AdventurePartnerMinimized(): # partnerImage="Mods/AdventurePartners/GUI/blankPixel.png"
  frame id "partnerMinimizedFrame":
    xpos -3 # -55
    ypos 167
    # yalign 0.2 # 0.35
    at partnerSize80
    background "Mods/AdventurePartners/GUI/blankPixel.png"
    imagebutton:
      idle "Mods/AdventurePartners/GUI/partner_minimized_sidebar.png"
      focus_mask True
      action [Hide("AdventurePartnerMinimized"), Show("AdventurePartnerScreen"), Function(renpy.log,"Minimized partner sidebar clicked.")]
      at transform:
        align (0.2, 0.5) alpha 0.0
        linear 0.25 alpha 1.0



# ---------------------------------------------------
# This is what will create the partner's imagebutton.
# ---------------------------------------------------
screen PartnerCard():
  # Check to see if this partner has a picture. Probably not relevant, but it was in the original code, so I'm including it.
  python:
    picCheck = 0
    try:
      if(adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet[0].name != "" and  adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet[0].name != "None"):
        picCheck = 1
    except:
      pass
  # End Python
  
  
  # frame id "partnerPictureFrame":
    # background "Mods/AdventurePartners/GUI/blankPixel.png"
    # at partnerPosition
    # at transform:
    #   alpha 0.5
  if(picCheck == 0 or persistent.showCharacterImages == False):
    # $ renpy.log("Debug: Attempted to load partner without an ImageSet.")
    pass
  else: # If it has a valid image set.
    $ bodyX = adventurePartner.positionImage[0]
    $ bodyY = 0
    $ xMonPos = 0
    $ yMonpos = 0
    
    # --- Red's Note: I'm completely scrapping the old way of doing images and rewriting it. ---
    $ adventurePartner.getPartnerImages()
    $ transformsList = []
    $ monsterToolTip = adventurePartner.name + ", " + adventurePartner.species + " " + adventurePartner.gender + " (level " + str(adventurePartner.stats.lvl) + ")\n" + adventurePartner.tooltipDesc
        
    if(len(adventurePartner.cropImage) == 4):
      $transformsList.append(crop(adventurePartner.cropImage[0], adventurePartner.cropImage[1], adventurePartner.cropImage[2], adventurePartner.cropImage[3]))
    if(adventurePartner.flipImage):
      $ transformsList.append(partnerFlip)
    $ transformsList.append(partnerSize80)
    $ transformsList.append(opaque)
    
    for img in adventurePartner.partnerImages:
      imagebutton:
        idle img[0]
        hover img[0]
        insensitive img[0]
        focus_mask True
        xpos img[1]
        xoffset adventurePartner.positionImage[0]
        ypos img[2]
        yoffset adventurePartner.positionImage[1]
        at transformsList
        action Function(adventurePartner.pester)
        # Tooltip section.
        hovered SetVariable("cmenu_tooltip", monsterToolTip)
        unhovered SetVariable("cmenu_tooltip", "")
    
    # --- Old Way ---
    # for layers in adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet:
      # I combined a few oddly nested if-statements in the original code.
      # if(len(layers.Images) >= 1 and layers.currentImage == 0):
        # if(layers.AlwaysOn == 1): # If the layers aren't meant to be toggleable overlays...
          # $ layers.currentImage = 1
        # else:
          # if(layers.Overlay != "No" and layers.Overlay != ""):
            # $ overlaying = getFromName(settingToImage, adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet)
            
            # $ overlaySet = adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet[overlaying]
            
            # $ layers.currentImage = getFromName(overlaySet.Images[overlaySet.currentImage].name,layers.Images)
            # $ layers.overlayOn = 1
      # End if
      
      # Here's the original code, which I find to be a lot less intelligible.
      # $ layersImagesLength = len(layers.Images) # Not needed anymore.
      # if(layers.currentImage == 0 and layersImagesLength >= 1 and layers.AlwaysOn == 1):
      #   $ layers.currentImage = 1
      # 
      # if(layers.Overlay != "No" and layers.Overlay != ""):
      #   if(layersImagesLength >= 1 and layers.currentImage == 0):
      #     $ overlaying = getFromName(settingToImage, adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet)
      #     $ layers.currentImage = getFromName(adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet[overlaying].Images[adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet[overlaying].currentImage].name, layers.Images)
      #     $ layers.overlayOn = 1
      
      # Set body x/y-alignment.
      # if(layers.TheBody == 1):
      #   $ bodyX = layers.setXalign
      #   $ bodyY = layers.setYalign
    # End for-loop
    
    # for layers in adventurePartner.ImageSets[adventurePartner.currentSet].ImageSet:
      # $ showimage = 1
      
      # # See if we should display the image on this layer.
      # if(layers.overlayOn == 0 and layers.Overlay != "No" and layers.Overlay != ""):
        # $ showimage = 0
      # elif(layers.player == "Yes"): # This elif and the next one appear to be another instance of needing to standardize your terminology.
        # if(PlayerDisplay == "Silhouette"):
          # $ showimage = 0
      # elif(layers.player == "Silhouette"):
        # if(PlayerDisplay == "Body"):
          # $ showimage = 0
      
      # if(showimage == 1 and layers.IsScene == 0): # and layers.currentImage > 0
        # # See if we need to animate stuff.
        # if(layers.animating == "Animation"):
          # $ imageShown = "animatingLayer"
        # elif(layers.animating == "Animation2"):
          # $ imageShown = "animatingLayer2"
        # elif(layers.animating == "Animation3"):
          # $ imageShown = "animatingLayer3"
        # else:
          # $ imageShown = layers.Images[layers.currentImage].file
        
        # # Apply some transforms if the player is present.
        # # Isn't it wonderful how they did this differently than 21 lines above?!
        # # if(layers.player == "Yes" or layers.player == "Silhouette"):
        # #   if(PlayerDisplay == "Body"):
        # #     $ transformsList = [CharacterBrightness, CharacterColor, CharacterOpacity, CharacterTint, CharacterSaturation]
        # #   else:
        # #     $ transformsList = [CharacterSilBrightness, CharacterSilColor, CharacterSilOpacity, CharacterSilTint,  CharacterSilSaturation]
        # # else:
        # #   $ transformsList = []  
        # # $ transformsList.append(characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos))
    
    # Won't have player images as part of the partner images, so ignoring that part.
    # $ transformsList = []
        
    # if(len(adventurePartner.cropImage) == 4):
      # $transformsList.append(crop(adventurePartner.cropImage[0], adventurePartner.cropImage[1], adventurePartner.cropImage[2], adventurePartner.cropImage[3]))
    # if(adventurePartner.flipImage):
      # $ transformsList.append(partnerFlip)
    # $ transformsList.append(partnerSize80)
    # $ transformsList.append(opaque)
        
        
        
        
        # I'm removing these animations, as I don't want the partner's image to bounce out of the box.
        # if(GlobalMotion != "" or layers.motion != "":)
          # if GlobalMotion == "Bounce" or layers.motion == "Bounce":
            # $ transformsList.append(Bounce)
          # elif GlobalMotion == "BounceSlow" or layers.motion == "BounceSlow":
            # $ transformsList.append(BounceSlow)
          # elif GlobalMotion == "BounceFast" or layers.motion == "BounceFast":
            # $ transformsList.append(BounceFast)
          # elif GlobalMotion == "BounceOnce" or layers.motion == "BounceOnce":
            # $ transformsList.append(BounceOnce)
          # elif GlobalMotion == "BounceCustom" or layers.motion == "BounceCustom":
            # $ transformsList.append(BounceCustom)
          # elif GlobalMotion == "Sway" or layers.motion == "Sway":
            # $ transformsList.append(Sway)
          # elif GlobalMotion == "SwaySlow" or layers.motion == "SwaySlow":
            # $ transformsList.append(SwaySlow)
          # elif GlobalMotion == "SwayFast" or layers.motion == "SwayFast":
            # $ transformsList.append(SwayFast)
          # elif GlobalMotion == "SwayOnce" or layers.motion == "SwayOnce":
            # $ transformsList.append(SwayOnce)
          # elif GlobalMotion == "SwayCustom" or layers.motion == "SwayCustom":
            # $ transformsList.append(SwayCustom)
          # elif GlobalMotion == "Pump" or layers.motion == "Pump":
            # $ transformsList.append(Pump)
          # elif GlobalMotion == "PumpSlow" or layers.motion == "PumpSlow":
            # $ transformsList.append(PumpSlow)
          # elif GlobalMotion == "PumpFast" or layers.motion == "PumpFast":
            # $ transformsList.append(PumpFast)
          # elif GlobalMotion == "PumpCustom" or layers.motion == "PumpCustom":
            # $ transformsList.append(PumpCustom)
          # elif GlobalMotion == "Ride" or layers.motion == "Ride":
            # $ transformsList.append(Ride)
          # elif GlobalMotion == "RideSlow" or layers.motion == "RideSlow":
            # $ transformsList.append(RideSlow)
          # elif GlobalMotion == "RideFast" or layers.motion == "RideFast":
            # $ transformsList.append(RideFast)
          # elif GlobalMotion == "RideCustom" or layers.motion == "RideCustom":
            # $ transformsList.append(RideCustom)
          # elif GlobalMotion == "Vibrate" or layers.motion == "Vibrate":
            # $ transformsList.append(Vibrate)
          # elif GlobalMotion == "VibrateCustom" or layers.motion == "VibrateCustom":
            # $ transformsList.append(VibrateCustom)
          # elif GlobalMotion == "Realign" or layers.motion == "Realign":
            # $ transformsList.append(Realign)
        
        # $ monsterToolTip = adventurePartner.name + ", " + adventurePartner.species + " " + adventurePartner.gender + " (level " + str(adventurePartner.stats.lvl) + ")\n" + adventurePartner.tooltipDesc
        # imagebutton:
          # idle imageShown
          # hover imageShown
          # insensitive imageShown
          # xpos adventurePartner.positionImage[0]
          # ypos adventurePartner.positionImage[1]
          # if len(transformsList) > 0:
            # at transformsList
          # action Function(adventurePartner.pester)
          # # Tooltip section.
          # hovered SetVariable("cmenu_tooltip", monsterToolTip)
          # unhovered SetVariable("cmenu_tooltip", "")
      # elif(layers.IsScene == 1):
        # pass # There was a whole other for-loop that dealt with scene images. It should have been included in this loop, in the first place, but I'm not using any scene images as partner images, so I can cut it out entirely.
    
    # This has something to do with the tooltip, but I'm not exactly sure what. I'm guessing that it creates the buttons under the targets when the player has to select the target for an ability. If so, it won't be needed here unless the player is a sadist who likes attacking his partner!
    
    # if(target == -1):
    #   imagebutton:
    #     hovered SetVariable("cmenu_tooltip", monsterToolTip)
    #     unhovered SetVariable("cmenu_tooltip", "")
    #     idle "blankButton.png"
    #     hover "blankButton.png"
    #     insensitive "blankButton.png"
        # yalign 0.4
        # xalign 0.5
    #     xpos 0 # adventurePartner.positionImage[0]
    #     ypos 0 # adventurePartner.positionImage[1]
    #     xsize 400 # 225
    #     ysize 800 # 300
    #     action SetVariable("cmenu_tooltip", ""), renpy.curry(renpy.end_interaction)(True)
    #     at partnerPosition
        # at characterPlacement(yMonpos, bodyY, bodyX, 0, xMonPos)
        #yalign adventurePartner.pictures[adventurePartner.currentPicture].setYalign
        #at CharacterZoom
    # End for-loop
    # --- End of the Old Display Code ---
    use PartnerHealthDisplay()

screen PartnerHealthDisplay():
  zorder 100
  
  # Calculate Variables
  python:
    adventurePartner.stats.Update()
    yAdjust = 1018 # 1038 to align with bottom of bg frame
    AP_Pct = max(0, float(adventurePartner.stats.hp)/adventurePartner.stats.max_true_hp)
    EP_Pct = max(0, float(adventurePartner.stats.ep)/adventurePartner.stats.max_true_ep)
    AP_crop = int(37 + (AP_Pct*225))
    EP_crop = int(37 + (EP_Pct*225))
    if adventurePartner.stats.max_true_sp > 0:
      spiritPct = adventurePartner.stats.sp/(adventurePartner.stats.max_true_sp+0.0)
    else:
      spiritPct = 0
    SPCropHeight = int(spiritPct*67)
    SPCropStart = 79 - SPCropHeight
  
  # Displayable Frame
  frame id "partnerHealthFrame":
    background Null()
    at transform:
      zoom 0.5
    
    fixed:
      xpos -504
      ypos  yAdjust +68
      add "gui/playerback.png"
    fixed:
      xsize 270
      ysize 270
      xpos 176
      ypos yAdjust
      at rotateHP
      add "gui/HP.png" crop (270-AP_crop, 0, AP_crop, 270) xpos 270-AP_crop
      add "gui/HPBar.png"
    fixed:
      xsize 270
      ysize 270
      xpos 428
      ypos yAdjust
      at rotateMP
      add "gui/MP.png" crop (270-EP_crop, 0, EP_crop, 270) xpos 266-EP_crop
      add "gui/MPBar.png"
    fixed: # HP Text
        xsize 200
        ysize 24
        xpos 270 -80 # 164
        ypos yAdjust
        # Charcoal Background
        text "{color=#111}[adventurePartner.stats.hp]/[adventurePartner.stats.max_true_hp]{/color}":
          size 36
          xalign 1.0
        # Colored Text
        text "{color=#ff587d}[adventurePartner.stats.hp]/[adventurePartner.stats.max_true_hp]{/color}":
          size 36
          xalign 1.0
        at rotateAPText
    fixed: # Energy Text
        xsize 200
        ysize 24
        xpos 270 +274 # 560
        ypos yAdjust
        # Charcoal Background
        text "{color=#111}[adventurePartner.stats.ep]/[adventurePartner.stats.max_true_ep]{/color}":
          size 36
        # Colored Text
        text "{color=#4BF}[adventurePartner.stats.ep]/[adventurePartner.stats.max_true_ep]{/color}":
          size 36
        at rotateEPText
    add "gui/SpiritFill.png":
      crop(0, SPCropStart, 96, SPCropHeight+12)
      xpos 406
      ypos yAdjust +SPCropStart +106
    imagebutton:
      xpos 406
      ypos yAdjust +108
      # focus_mask True
      idle "gui/SpiritBack.png"
      hover "gui/SpiritBack.png"
      hovered SetVariable("cmenu_showHealthTooltip", True)
      unhovered SetVariable("cmenu_showHealthTooltip", False)
      if MenuLineSceneCheckMark == -1 and inTownMenu == 0 and npcCount == 0  and senCount == 0 and fetCount == 0:
        action renpy.curry(renpy.end_interaction)(True)
      else:
        action [SelectedIf(False), NullAction()] #make hoverable  
    if cmenu_showHealthTooltip: # Spirit Text
      # Charcoal Background
      text "{color=#111}[adventurePartner.stats.sp]/[adventurePartner.stats.max_true_sp]{/color}":
        size 36
        xpos 426
        ypos yAdjust +132
      # Colored Text
      text "{color=#DFD}[adventurePartner.stats.sp]/[adventurePartner.stats.max_true_sp]{/color}":
        # size 25
        # xpos 433
        # ypos yAdjust +132
        size 36
        xpos 426
        ypos yAdjust +132
    else:
      # Charcoal Background
      text "{color=#111}[adventurePartner.stats.sp]{/color}":
        size 36
        xpos 442
        ypos yAdjust +132
      # Colored Text
      text "{color=#DFD}[adventurePartner.stats.sp]{/color}":
        # size 27
        # xpos 445
        # ypos yAdjust +132
        size 36
        xpos 442
        ypos yAdjust +132
  # Add status effects over adventurePartner icon
  # use StatusBar(adventurePartner) #it's in on_enemyCardScreen.rpy
  # use ON_CombatMenuTooltip
