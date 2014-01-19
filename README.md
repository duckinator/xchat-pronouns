# Preferred pronouns script #

* `/PRONOUNS <handle>`
    <p>Get the preferred pronouns for `<handle>`, if they have it specified in their IRC realname string.</p>
* `/SETPRONOUNS <pronouns>`
    <p>Set your own preferred pronouns. `<pronouns>` can be whatever text you'd like. Requires reconnecting to take effect.</p>
    <p>If you don't pass any arguments it returns your currently-configured pronouns.</p>

## Setup ##

Assuming you pronouns are singular they, and your handle on IRC is `foobar`:

    /setpronouns they

Reconnect.

    /pronouns foobar

It should return your preferred pronouns as you entered them.

## Notes

Due to how this is implemented (using realname field), you have to reconnect (or restart XChat) for changes to your preferred pronouns to take effect.
