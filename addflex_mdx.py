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
       description='Convert inflections from a table to the MDX source file (.txt)',
       formatter_class=argparse.RawTextHelpFormatter,
       epilog = '''example:
 %(prog)s -t forms-BG.txt -o mdx_addon_file.txt 
 '''
 )
parser.add_argument('-o', '--output', dest='dictOut', metavar='FILENAME', required=True,
                    action='store', 
                    help='MDX inflections file that should be concatenated to the MDX dictionary itself')
parser.add_argument('-t', '--table', dest='flexFile', metavar='FILENAME', required=True,
                    action='store', 
                    help='flexion file (format "stem: form, form, form...")')
parser.add_argument('-l', '--link', dest='is_link',
                    action='store_true', default=False,
                    help='generate @@@LINKS instead of cards with ref')

args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

flexFile = args.flexFile
dictOut  = args.dictOut

inflDict = None

print( f'Parsing inflections from "{flexFile}"' ) 
with open( flexFile, encoding='utf8' ) as inflF:
    inflDict = read_wordforms_as_list( inflF )

if inflDict:
    print( f'Creating dictionary file -> "{dictOut}"' )
    with open( dictOut, "w", encoding='utf8' ) as outF:
        for stem in inflDict:
            flexes = sorted(list(inflDict[stem]))
            for flex in flexes:
                if args.is_link:
                    print( f'{flex}\n@@@LINK={stem}\n\n</>', file=outF )
                else:
                    print(f'{flex}\n{flex} ⇒ <a href="entry://{stem}">{stem}</a>\n\n</>', file=outF)
else:
    print("Input wordlist is empty - check wordlist format", file=sys.stdout)
