## Information
<a href='https://btagscript.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/btagscript/badge/?version=latest' alt='Documentation Status' />
</a>
<img width="851" alt="bTagScriptBasic" src="https://user-images.githubusercontent.com/57199957/178122657-98041f02-0009-43d0-9c38-e12c2219e3a6.png">

This repository is a fork of Phenom4n4n's fork of JonSnowbd's [TagScript](https://github.com/JonSnowbd/TagScript), a string templating language.

Documentation on the bTagScript library can be [found here](https://btagscript.readthedocs.io/en/latest/).

## Benchmarks (Performance Testing)

### July 08, 2022

Testing for this benchmark used the following seeds and test strings, this was ran `1,000` times.

```yaml
Seeds: {message: Hello, this is my message.}
Test String: {message} {#:1,2,3,4,5,6,7,8,9,10} {range:1-9} {$variablename:Hello World} {variablename} {message} {strf:Its %A}
```

Note that this was adjusted for different syntax, {=(variablename):Hello World}

```
2.6.9 bTagScript
0.08033132553100586 Seconds

2.6.2 TagScript
0.08630657196044922 Seconds
```

## What?

TagScript allows you to create low level code, quickly, and easily. This is meant to be used with discord.py 2.0 and is not compatible with other versions.

## Dependencies

`Python 3.8+`

`discord.py`

`pyparsing`


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
