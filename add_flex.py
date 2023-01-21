import sys
import argparse

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

