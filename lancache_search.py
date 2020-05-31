from glob import glob
from os.path import isfile
from os import remove
from argparse import ArgumentParser
from sys import stdout
from logging import basicConfig,DEBUG,INFO,WARNING,ERROR
from logging import debug,info,warning,error
#import logging as logger

## Init some stuff
KEY          = "KEY:".encode('utf-8')
count_hits   = 0
count_files  = 0
hit_files    = []

## Configure the program arguments
parser = ArgumentParser("This prgram helps you find LanCache cache-files associated with certain content and remove them.")
parser.add_argument("-p", "--path", help="The path of the LanCache cache-files. Please specify either --path or --read. In case both parameters are given, --path will be ignored.")
parser.add_argument("-P", "--pattern", help="The pattern to look for in the cache-files. If no pattern is given, all files will be returned.", default="")
parser.add_argument("-r", "--read", help="Read previous stored search result from the given input file. Please specify either --path or --read. In case both parameters are given, --path will be ignored.")
parser.add_argument("-w", "--write", help="Write the results of the search to the given output file.")
parser.add_argument("-d", "--delete", help="Remove the matched files from the LanCache cache. Please also specify option --read or --pattern.", action='store_true')
parser.add_argument("-l", "--loglevel", help="Set the log-level. Default: info", default="info", choices=["debug","info","warning","error"])
args = parser.parse_args()

## Set log-level
if args.loglevel=="debug":
    loglevel = DEBUG
elif args.loglevel=="info":
    loglevel = INFO
elif args.loglevel=="warning":
    loglevel = WARNING
elif args.loglevel=="error":
    loglevel = ERROR
FORMAT = '%(asctime)s %(levelname)s LanCache_Search %(message)s'
basicConfig(stream=stdout, level=loglevel, format=FORMAT)

## Read / Validate the parameters
if args.read:       # Get the filenames from the input file
    if args.path:
        warning("Both --path and --read are given. Option --path will be ignored!")

    fp = open(args.read, 'r')
    info("Input file opened: " + args.read)
    files = []
    while True:
        line = fp.readline()
        if not line:
            break
        filename = line.split("||")[0]
        files.append(filename)
    fp.close()
    info("Finished reading input file. Read files: " + str(len(files)))
    info("Input file closed: " + args.read)
elif args.path:     # Read the filenames from the given path
    info("Creating file list, from path: " + args.path)
    files = glob(args.path+"/**/*", recursive=True)
    info("File list created")
else:               # Error, I have no filenames!
    error("Specifiy one of the following options: --path (-p) or --read (-r)")
    parser.print_help()
    quit(2)

# Verify and confirm the delete-option
if args.delete and not (args.pattern or args.read):
    error("Please use the --delete option on combination with: --read (-r) and/or --pattern (-P)")
    parser.print_help()
    quit(2)
elif args.delete:
    print("You set the option --delete, THIS WILL DELETE ALL MATCHED FILES!")
    print("Are you sure? Type \"YES\" to confirm: ", end="")
    confirm = input()
    if confirm!="YES":
        error("Option --delete is not confirmed, the script will exit now!")
        quit(2)
    else:
        info("Option --delete was confirmed correctly.")


## Open the output-file for writing
if args.write:
    fp_output = open(args.write, 'w')
    info("Output file opened: " + args.write)

## The main search loop
for file in files:
    if not isfile(file):
        continue        # Skip everything that is not a file, for example directories

    loop_count  = 0
    count_files = count_files + 1

    fp   = open(file, 'rb')
    line = fp.readline()

    while (not(line[:4] == KEY) and loop_count < 5):
        line       = fp.readline()
        loop_count = loop_count + 1

    fp.close

    if not loop_count < 5:
        debug("No match found for: " + file)
        continue

    line = line.decode('utf-8').rstrip()
    if (args.pattern in line):
        if args.write:
            fp_output.write(file + "||" + line + "\n")
        debug("Match file: " + file + "||" + line)
        hit_files.append(file)
        count_hits = count_hits + 1
    
info("Number of files: "+str(count_files))
info("Number of hits: "+str(count_hits))
info("Number of misses: "+str(count_files-count_hits))

## Close the output-file
if args.write:
    fp_output.close()
    info("Output file closed: " + args.write)

## Delete files
if args.delete and confirm == "YES":
    for hit_file in hit_files:
        info("DELETE file: " + hit_file)
        remove(hit_file)

