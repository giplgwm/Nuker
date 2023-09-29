# Nuker
  The original idea of this project was to learn the shelve module and how to restore objects from it. As such this bot can backup/remove/restore the following:
  Channels,
  Categories,
  Emojis,
  Logo,
  Banner,
  Server Name.
  After that was working i was wondering about a ransom-style attack where the bot requests a payment and restores the channel after. For now it sends the payment link, but getting stripe webhooks working with flask is stumping me. For now the $restore command is available by default (for anyone in the server).
  
  # Usage
  set 'token' to your discord bot token, 'payment_link' as your payment link, change settings in config as desired. Default behaviour is to backup server on join, nuke, and send payment link to every spam text channel created. Turn this behaviour off with b_extort.
