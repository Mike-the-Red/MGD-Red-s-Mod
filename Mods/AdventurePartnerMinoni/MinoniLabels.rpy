# Partner Specific Variables
default minoniPartnerChain = 0

label minoniPesterOne:
  "Minoni" "Hi, [player.name]."
  menu:
    "I'm glad we're traveling together.":
      $ adventurePartner.showPartnerImage("Smile")
      $ adventurePartner.showPartnerImage("Base","EarR")
      $ adventurePartner.showPartnerImage("Base","EarL")
      "Minoni" "So am I. Working at the temple is nice, and it gives me plenty of time to read, but there's nothing quite like the feeling of putting your hooves to trail and traveling."
    "We should split up, for now.":
      $ adventurePartner.showPartnerImage("Shy")
      $ adventurePartner.showPartnerImage("Base","ArmR")
      $ adventurePartner.showPartnerImage("Droop","EarR")
      $ adventurePartner.showPartnerImage("Droop","EarL")
      "Minoni" "Ah. Well, it's probably time for me to head back to the Temple of Will-Power, anyway."
      $ partnerName = ""
      $ adventurePartner = AdventurePartner()
  return

