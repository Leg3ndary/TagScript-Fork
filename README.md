## Information
<a href='https://tagscript.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/tagscript/badge/?version=latest' alt='Documentation Status' />
</a>
<a href='https://pypi.python.org/pypi/TagScript/'>
    <img src='https://img.shields.io/pypi/v/TagScript' alt=' yPI' />
</a>

This repository is a fork of JonSnowbd's [TagScript](https://github.com/JonSnowbd/TagScript), a string templating language.
This fork adds support for Discord object adapters and a couple Discord related blocks, as
well as multiple utility blocks. Additionally, several tweaks have been made to the engine's
behavior.

This TagScriptEngine is used on [Noumenon, a Discord bot](https://discordapp.com/oauth2/authorize?client_id=634866217764651009&permissions=2080894207&scope=bot%20applications.commands).
An example implementation can be found its [Tags cog](https://github.com/phenom4n4n/phen-cogs/tree/master/tags).

Additional documentation on the TagScriptEngine library can be [found here](https://tagscript.readthedocs.io/en/latest/).

## Installation

Download the latest version through github:

```
pip(3) install https://github.com/Leg3ndary/bTagScript
```

Download from a commit:

```
pip(3) install git+https://github.com/Leg3ndary/bTagScript.git@<COMMIT_HASH>
```

Install for editing/development:

```
git clone https://github.com/Leg3ndary/bTagScript.git
pip(3) install -e ./bTagScript
```

## What?

TagScript allows you to create low level code, quickly, and easily. This is meant to be used with discord.py 2.0 and is not compatible with other versions.

## Dependencies

`Python 3.8+`
`discord.py`
`pyparsing`
