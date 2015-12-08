import xchat, re

__module_name__ = "xchat-pronouns"
__module_version__ = "0.1"
__module_description__ = "Set information about your personal pronouns, and fetch information about others' personal pronouns."

pronouns_regexp = " \\[pronouns: (.*)\\]$"

capture_whois = False
def cb_whois_common(word, word_eol, userdata):
    if capture_whois:
        return xchat.EAT_ALL
    else:
        return xchat.EAT_NONE

def cb_whois_name_line(word, word_eol, userdata):
    pronouns = get_pronouns(word_eol[3])

    if pronouns:
        xchat.prnt("Pronouns for " + word[0] + ": " + pronouns + ".")
    else:
        xchat.prnt(word[0] + " has not specified their pronouns.")

    return xchat.EAT_ALL

def cb_whois_end(word, word_eol, userdata):
    global capture_whois

    capture_whois = False

    return xchat.EAT_ALL

for event in ["Authenticated", "Away Line", "Channel/Oper Line", "Identified", "Idle Line", "Idle Line with Signon", "Real Host", "Server Line", "Special"]:
    xchat.hook_print("WhoIs " +  event, cb_whois_common)

xchat.hook_print("Whois Name Line", cb_whois_name_line)
xchat.hook_print("Whois End", cb_whois_end)

def real_name():
    return xchat.get_prefs("irc_real_name")

def set_real_name(new_real_name):
    xchat.command("set irc_real_name " + new_real_name)

# Given a string, return the pronouns from it.
def get_pronouns(string):
    m = re.search(pronouns_regexp, string, flags=re.IGNORECASE)
    if m is None:
        return None
    else:
        return m.group(1)

# Given a string, strip pronouns from it.
def strip_pronouns(string):
    pronouns = get_pronouns(string)

    # Take everything before the pronouns, if any are in the string.
    if pronouns:
        string = string[0:(len(string) - len(pronouns) - 13)]
    return string

# Return the pronouns set locally.
def my_pronouns():
    return get_pronouns(real_name())

# Set pronouns to the specified string.
def set_pronouns(new_pronouns):
    base_real_name = strip_pronouns(real_name())

    pronouns_text = " [pronouns: " + new_pronouns + "]"

    new_real_name = base_real_name + pronouns_text

    if len(new_real_name) > 50:
        xchat.prnt("The total length for your \"real name\" setting must be at most 50 characters.")
        xchat.prnt("Setting your pronouns to \"" + new_pronouns + "\" would make it " + str(len(new_real_name)) + " characters.")
        xchat.prnt("Go to XChat, then Network List, put a shorter value in the \"Real name\" box, and then try again")
        return False
    else:
        set_real_name(new_real_name)
        return True

def get_others_pronouns(handle):
    global capture_whois

    capture_whois = True
    xchat.command("WHOIS " + handle)

    return xchat.EAT_ALL

pronouns_usage = "Usage: PRONOUNS <handle>, get the pronouns for <handle>, if they have it specified in their IRC realname string."
def cmd_pronouns(word, word_eol, userdata):
    if len(word) > 1:
        get_others_pronouns(word[1])
    else:
        xchat.prnt(pronouns_usage)
    return xchat.EAT_ALL

setpronouns_usage = "Usage: SETPRONOUNS <pronouns>, Set your own pronouns. <pronouns> can be whatever text you'd like. Requires reconnecting to take effect.\nIf <pronouns> is not specified, returns your currently-configured pronouns."
def cmd_setpronouns(word, word_eol, userdata):
    if len(word_eol) >= 2:
        if set_pronouns(word_eol[1]):
            xchat.prnt("Pronouns set to: " + my_pronouns())
    else:
        if my_pronouns():
            xchat.prnt("Your pronouns are currently set to: " + my_pronouns())
        else:
            xchat.prnt("You haven't set your pronouns yet!")
            xchat.prnt("If you're not sure how, run /help SETPRONOUNS.")
    return xchat.EAT_ALL

unsetpronouns_usage = "Usage: UNSETPRONOUNS, Unset your pronouns."
def cmd_unsetpronouns(word, word_eol, userdata):
    set_real_name(strip_pronouns(real_name()))
    xchat.prnt("Your pronouns have been unset.")
    return xchat.EAT_ALL

xchat.prnt("Pronouns script initialized")

xchat.hook_command("PRONOUNS", cmd_pronouns, help=pronouns_usage)
xchat.hook_command("SETPRONOUNS", cmd_setpronouns, help=setpronouns_usage)
xchat.hook_command("UNSETPRONOUNS", cmd_unsetpronouns, help=unsetpronouns_usage)
xchat.hook_command("CLEARPRONOUNS", cmd_unsetpronouns, help=unsetpronouns_usage)



def whois_callback(word, word_eol, userdata):
    global capture_whois

    if capture_whois:
        return xchat.EAT_NONE

    # Response format:
    # :server 311 yournick othersnick ~othersuser others/host * :Other's Realname

    _, _, _, nickname, username, host = word[0:6]
    raw_real_name = word_eol[7][1:]

    # Get the real name without pronouns. If they don't have their pronouns
    # specified in their WHOIS information, it simply shows their real name
    # string as-is.
    real_name = strip_pronouns(raw_real_name)

    # Get their pronouns, or None.
    pronouns = get_pronouns(raw_real_name)

    # Print the first line of the WHOIS response, sans pronouns snippet at the end,
    # exactly how XChat would print it otherwise.
    xchat.emit_print("WhoIs Name Line", nickname, username, host, real_name)

    # Print their pronouns as the second line of the WHOIS information,
    # if they specified anything. Otherwise, do nothing.
    if pronouns is not None:
        xchat.emit_print("WhoIs Identified", nickname, "Pronouns: " + pronouns)

    # Stop XChat from printing the default first WHOIS line.
    return xchat.EAT_XCHAT

xchat.hook_server("311", whois_callback)
