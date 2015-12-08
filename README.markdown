# Personal pronouns script

* `/PRONOUNS <handle>` (not yet implemented)
    <p>Get the pronouns for `<handle>`, if they have it specified in their IRC realname string.</p>
* `/SETPRONOUNS <pronouns>`
    <p>Set your own pronouns. `<pronouns>` can be whatever text you'd like. Requires reconnecting to take effect.</p>
    <p>If you don't pass any arguments it returns your currently-configured pronouns.</p>
* `/UNSETPRONOUNS` (alias: `/CLEARPRONOUNS`)
    <p>Clear any pronouns you have specified.</p>

## WHOIS

`xchat-pronouns` also ties into WHOIS replies, and adds a line starting with "Pronouns:" for anyone who specifies them.

Example:

```
* [duckinator] (~duckie@unaffiliated/duckinator): Marie Markwell
* [duckinator] Pronouns: they/them/themself
* [duckinator] hitchcock.freenode.net :Sofia, BG, EU
* duckinator :is using a secure connection
* [duckinator] is logged in as duckyy
* [duckinator] End of WHOIS list.
```

## Setup

Assuming your pronouns are singular they, and your handle on IRC is `foobar`:

    /setpronouns they/them/their

Reconnect.

    /whois foobar

The WHOIS response for yourself should include your pronouns as you entered them.

## Notes

Due to how this is implemented (using realname field), you have to reconnect (or restart XChat) for changes to your pronouns to take effect.
