import xchat, dbus, os, inspect, re

__module_name__ = "xchat-pronouns"
__module_version__ = "0.1"
__module_description__ = "Set information about your personal pronouns, and fetch information about others' personal pronouns."

pronouns_regexp = " \\[pronouns: (.*)\\]$"

def set_real_name(realname):
  xchat.command("set irc_real_name " + realname)

def get_pronouns():
  irc_real_name = xchat.get_prefs("irc_real_name")
  m = re.search(pronouns_regexp, irc_real_name, flags=re.IGNORECASE)
  if m is None:
    return None
  else:
    return m.group(1)

def get_realname_without_pronouns():
  irc_real_name = xchat.get_prefs("irc_real_name")
  pronouns = get_pronouns()
  
  # The 14 is to account for for " [pronouns: ]".
  if pronouns:
    irc_real_name = irc_real_name[0:(len(irc_real_name) - len(pronouns) - 13)]
  
  return irc_real_name

def set_pronouns(new_pronouns):
  irc_real_name = get_realname_without_pronouns()
  
  pronouns_text = " [pronouns: " + new_pronouns + "]"
  
  new_real_name = irc_real_name + pronouns_text
  
  if len(new_real_name) > 50:
    xchat.prnt("The total length for your \"real name\" setting must be at most 50 characters.")
    xchat.prnt("Setting your preferred pronouns to \"" + new_pronouns + "\" would make it " + str(len(new_real_name)) + " characters.")
    xchat.prnt("Go to XChat, then Network List, put a shorter value in the \"Real name\" box, and then try again")
    return False
  else:
    set_real_name(irc_real_name + pronouns_text)
    return True

def get_others_pronouns(handle):
  return "Not implemented."

pronouns_usage = "Usage: PRONOUNS <handle>, get the preferred pronouns for <handle>, if they have it specified in their IRC realname string."
def cmd_pronouns(word, word_eol, userdata):
  if len(word) > 0:
    xchat.prnt("[Not implemented.]")
  else:
    xchat.prnt(pronouns_usage)
  return xchat.EAT_ALL

setpronouns_usage = "Usage: SETPRONOUNS <pronouns>, Set your own preferred pronouns. <pronouns> can be whatever text you'd like. Requires reconnecting to take effect.\n                               If <pronouns> is not specified, returns your currently-configured pronouns."
def cmd_setpronouns(word, word_eol, userdata):
  if len(word_eol) >= 2:
    if set_pronouns(word_eol[1]):
      xchat.prnt("Pronouns set to: " + get_pronouns())
  else:
    pronouns = get_pronouns()
    if pronouns:
      xchat.prnt("Your pronouns are currently set to: " + pronouns)
    else:
      xchat.prnt("You haven't set your pronouns yet!")
      xchat.prnt("If you're not sure how, run /help SETPRONOUNS.")
  return xchat.EAT_ALL

unsetpronouns_usage = "Usage: UNSETPRONOUNS, Unset your preferred pronouns."
def cmd_unsetpronouns(word, word_eol, userdata):
  set_real_name(get_realname_without_pronouns())
  xchat.prnt("Your pronouns have been unset.")
  return xchat.EAT_ALL

xchat.prnt("Pronouns script initialized")

xchat.hook_command("PRONOUNS", cmd_pronouns, help=pronouns_usage)
xchat.hook_command("SETPRONOUNS", cmd_setpronouns, help=setpronouns_usage)
xchat.hook_command("UNSETPRONOUNS", cmd_unsetpronouns, help=unsetpronouns_usage)
xchat.hook_command("CLEARPRONOUNS", cmd_unsetpronouns, help=unsetpronouns_usage)
