# Partner Specific Variables
default kyraPartnerChain = 0

label KyraPester:
  "Kyra" "Yes, soulmate?"
  menu:
    "I'm glad we're traveling together.":
      $ adventurePartner.showPartnerImage("BaseBlush")
      "Kyra" "So am I. It's very hard to find a worthy mate."
    "We should split up, for now.":
      $ adventurePartner.showPartnerImage("Surprised")
      "Kyra" "Here?! Now?!"
      "[player.name]" "For now."
      $ adventurePartner.showPartnerImage("PanicBlush")
      "Kyra" "Oh, okay...."
      # $ adventurePartner.showPartnerImage("Hmph")
      $ partnerName = ""
      $ adventurePartner = AdventurePartner()
      "The lizard girl turns tail and runs away with impressive speed."
  return

