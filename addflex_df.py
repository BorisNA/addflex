import sys
import argparse
from typing import TextIO, Dict, Set


def read_wordforms_as_list( infile: TextIO ) -> Dict[ str, Set ]|None:
    is_error = False
    infl_dict = {}
    for line in infile:
        line = line.rstrip()
        spl = line.split(":")
        if len(spl) != 2:
            err = f'Wordform error at: "{line}"'
            if 'logging' in sys.modules:
                logging.error( err )
            else:
                print( err, file=sys.stderr )
            is_error = True
            continue

        stem, flex = spl
        stem = stem.strip()
        flex_line = flex.split(",")
        flex_line = (f.strip() for f in flex_line)
        flex_line = [f for f in flex_line if f != stem and f != '']
        if len(flex_line) > 0:
            # do not add empty sets
            if not infl_dict.get(stem):
                infl_dict[stem] = set()
            infl_dict[stem].update(flex_line)

    if is_error:
        infl_dict = None

    return infl_dict


parser = argparse.ArgumentParser(
       description='Add flections from a table to the Kobo dictionary file (.df)',
       formatter_class=argparse.RawTextHelpFormatter,
       epilog = '''example:
 %(prog)s -i dictionary.df -o dictionary_out.df -t forms-UK.txt
 '''
 )
parser.add_argument('-i', '--input', dest='dictFile', metavar='FILENAME', required=True,
                    action='store', 
                    help='input dictionary (Kobo dictfile .df)')
parser.add_argument('-o', '--output', dest='dictOut', metavar='FILENAME', required=True,
                    action='store', 
                    help='output dictionary filename')
parser.add_argument('-t', '--table', dest='flexFile', metavar='FILENAME', required=True,
                    action='store', 
                    help='flexion file (format "stem: form, form, form...")')

args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

flexFile = args.flexFile
dictFile = args.dictFile
dictOut  = args.dictOut

inflDict = {}

print( f'Parsing inflections from "{flexFile}"' ) 
with open( flexFile, encoding='utf8' ) as inflF:
    inflDict = read_wordforms_as_list( inflF )

if inflDict:
    print( f'Parsing dictionary file "{dictFile}" -> "{dictOut}"' )
    with open( dictFile, encoding='utf8' ) as dictF, \
         open( dictOut, "w", encoding='utf8' ) as outF:
        for line in dictF:
            line = line.strip()
            if line.startswith( '@' ):
                print( line, file = outF )
                word = line[2:].strip()
                for form in inflDict.get( word, {} ):
                    print( f'& {form}', file = outF )
            else:
                print( line, file = outF )
else:
    print("Input wordlist is empty - check wordlist format", file=sys.stdout)