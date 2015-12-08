# xchat-pronouns

This plugin also works with HexChat.

* `/PRONOUNS <handle>`
    <p>Get the pronouns for `<handle>`, if they have it specified in their IRC realname string.</p>
* `/SETPRONOUNS <pronouns>`
    <p>Set your own pronouns. `<pronouns>` can be whatever text you'd like. Requires reconnecting to take effect.</p>
    <p>If you don't pass any arguments it returns your currently-configured pronouns.</p>
* `/UNSETPRONOUNS` (alias: `/CLEARPRONOUNS`)
    <p>Clear any pronouns you have specified.</p>

## Setup

Assuming your pronouns are singular they:

    /setpronouns they/them/their

Your pronouns will be updated after reconnecting.

## WHOIS

`xchat-pronouns` also ties into WHOIS replies, and adds a line starting with "Pronouns:" for anyone who specifies them.

E.g., if you run `/whois duckinator` on FreeNode, you will get something along the lines of:

```
* [duckinator] (~duckie@unaffiliated/duckinator): Marie Markwell
* [duckinator] Pronouns: they/them/their
* [duckinator] hitchcock.freenode.net :Sofia, BG, EU
* duckinator :is using a secure connection
* [duckinator] is logged in as duckyy
* [duckinator] End of WHOIS list.
```

## /pronouns

If you run `/pronouns duckinator`, you should get:

```
Pronouns for duckinator: they/them/their.
```

## Notes

Due to how this is implemented (using realname field), you have to reconnect (or restart XChat) for changes to your pronouns to take effect.
