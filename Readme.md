# addflex

A simple way to add inflection forms to the StarDict dictionary (to use in KOreader, for example)

## Prerequisites

1. A dictionary in a parseable format, for example StarDict, DSL, XDXF etc (see notes on DSL below!)
2. Inflection forms file (for example from https://github.com/BorisNA/dsl2mobi/tree/master/wordforms)
3. A tool to convert the dictionary to the Kobo dictfile (.df) format and .df to the StarDict format (for example https://github.com/ilius/pyglossary)
4. Python ~~to rule them all~~ to run this script

## Adding inflections to the StarDict format

Since the `pyglossary` can not add inflections to a dictionary from a standalone file we need to convert the dictionary to a intermediate file that can be read/written by `pyglossary` *and* is easy to manipulate from the script.

### HOWTO

1. Convert a dictionary to the Kobo dictfile (.df) format.

   `pyglossary test.dsl test.df`

2. Add infections to the converted dictionary with the provided script **add_flex.py**. 

   `python add_flex.py -i test.df -o test_out.df -t forms-UK-test.txt`

3. Convert the resulting dictionary with inflections to the Stardict. Do not use `merge_syns` `pyglossary`'s option or the dictionary card title will be changed from the stem to the infected variant.

   `pyglossary test_out.df test_out.ifo --read-format=Dictfile --write-format=Stardict ''"'"'--json-write-options={"dictzip": true, "sametypesequence": "h", "merge_syns": false}'"'"'' `
   

## Notes on converting DSL dictionaries

DSL dictionaries often contain stress marks not only in the card body, but in the dictionary entry title (that is the index word) itself. Pyglossary, unfortunately, can not remove these stress marks and just adds them to the resulting file. And when converted to the StarDict format, StarDict engine is not able to match a word with its "stressed" definition.

Possible solution is to clear all stress marks in the source DSL file in text editor with the following regexp pattern.

```
\{\[/?'\]\}
```

## Inflection file format

Inflection file format is simple:

```
stem1: infected11, inflected12, inflected13, ...
stem2: infected21, inflected22, inflected23, ...
...

```

You can generate this file from hunspell or use from https://github.com/Tvangeste/dsl2mobi or  https://github.com/BorisNA/dsl2mobi (in the latter fork there are UK and alternative DE files)


