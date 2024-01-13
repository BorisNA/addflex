# Introduction to addflex

A collection of scripts to add inflection data to different dictionary formats

* Add inflections to StarDict (for KOreader for example) and possibly some other formats - see [Adding inflections to 
a StarDict dictionary thru DF file](#addflex_df)
* Add inflections to MDX filee - see [Adding inflections to a MDX dictionary](#addflex_mdx)


## Source inflection file format

Inflection file format is simple:

```
stem1: infected11, inflected12, inflected13, ...
stem2: infected21, inflected22, inflected23, ...
...

```

Wordforms files for selected languages are available at https://github.com/BorisNA/wordforms

## addflex_df

A simple way to add inflection forms to the StarDict dictionary (to use in KOreader, for example)

### Prerequisites

1. A dictionary in a parseable format, for example StarDict, DSL, XDXF etc (see notes on DSL below!)
2. Inflection forms file (see [Wordform file](#source-inflection-file-format))
3. A tool to convert the dictionary to the Kobo dictfile (.df) format and .df to the StarDict format (for example https://github.com/ilius/pyglossary)
4. Python ~~to rule them all~~ to run this script

### Adding inflections to the StarDict format

Since the `pyglossary` can not add inflections to a dictionary from a standalone file we need to convert the dictionary to a intermediate file that can be read/written by `pyglossary` *and* is easy to manipulate from the script.

#### HOWTO

1. Convert a dictionary to the Kobo dictfile (.df) format.

   `pyglossary test.dsl test.df`

2. Add infections to the converted dictionary with the provided script **add_flex.py**. 

   `python addflex_df.py -i test.df -o test_out.df -t forms-UK-test.txt`

3. Convert the resulting dictionary with inflections to the Stardict. Do not use `merge_syns` `pyglossary`'s option or the dictionary card title will be changed from the stem to the infected variant.

   `pyglossary test_out.df test_out.ifo --read-format=Dictfile --write-format=Stardict ''"'"'--json-write-options={"dictzip": true, "sametypesequence": "h", "merge_syns": false}'"'"'' `
   

### Notes on converting DSL dictionaries

DSL dictionaries often contain stress marks not only in the card body, but in the dictionary entry title (that is the index word) itself. Pyglossary, unfortunately, can not remove these stress marks and just adds them to the resulting file. And when converted to the StarDict format, StarDict engine is not able to match a word with its "stressed" definition.

Possible solution is to clear all stress marks in the source DSL file in text editor with the following regexp pattern.

```
\{\[/?'\]\}
```


## addflex_mdx

There are two options to generate morphological data for MDX

1. Create links for the dictionary, then if one searches for wordform, the card with the stem is automatically opened.
It is convenient, but the downside is that you need to regenerate every dictionary adding this "morphological delta"
2. Create a standalone dictionary, where for each wordform there is a card with the link to the stem. Downside is that
one need to click again on this link to get to the needed entry.

### Create a "morphological addon" with links

1. Create an inflection file for the desired language

   `python addflex_mdx.py -l -t forms-UK-test.txt -o test_MDX_infl.txt`

2. Concatenate this file with your source MDX file

   For example with `copy some_MDX_file.txt+test_MDX_infl.txt some_MDX_file_with_infl.txt`

3. Convert the concatenated file to every MDX needed

   For example with `mdict -a some_MDX_file_with_infl.txt some_MDX_file_with_infl.mdx`

### Create a standalone dictionary

1. Create a standalone inflection file for the desired language

   `python addflex_mdx.py -t forms-UK-test.txt -o test_MDX_infl_UK.txt`

2. Generate a "morphological dictionary" as usual

   For example with `mdict -a test_MDX_infl_UK.txt morphological_UK.mdx`
