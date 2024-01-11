import sys
import argparse

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

args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

flexFile = args.flexFile
dictOut  = args.dictOut

inflDict = {}

print( f'Parsing inflections from "{flexFile}"' ) 
with open( flexFile, encoding='utf8' ) as inflF:
    for line in inflF:
        try:
            base, flex = line.split(":")
            base = base.strip()
        except ValueError:
            print( line )
            exit
        flexL = flex.split(",")
        flexL = ( f.strip() for f in flexL )
        flexL = [ f for f in flexL if f != base ]
        inflDict[ base ] = flexL

print( f'Creating dictionary file -> "{dictOut}"' )
with open( dictOut, "w", encoding='utf8' ) as outF:
    for stem in inflDict:
        for flex in inflDict[ stem ]:
            print( f'{flex}\n@@@LINK={stem}\n\n</>', file=outF)

