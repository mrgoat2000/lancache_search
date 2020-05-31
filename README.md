# lancache_search

This prgram helps you find LanCache cache-files associated with certain content and remove them. Based on the cache-key you can easily find cache-files associated with certain cached content using the search pattern. This is usefull in case of a corrupt or stale cache-file.

This tool is based on Python3 and doesn't require additional packages.

usage:
       [-h] [-p PATH] [-P PATTERN] [-r READ] [-w WRITE] [-d]
       [-l {debug,info,warning,error}]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  The path of the LanCache cache-files. Please specify
                        either --path or --read. In case both parameters are
                        given, --path will be ignored.
  -P PATTERN, --pattern PATTERN
                        The pattern to look for in the cache-files. If no
                        pattern is given, all files will be returned.
  -r READ, --read READ  Read previous stored search result from the given
                        input file. Please specify either --path or --read. In
                        case both parameters are given, --path will be
                        ignored.
  -w WRITE, --write WRITE
                        Write the results of the search to the given output
                        file.
  -d, --delete          Remove the matched files from the LanCache cache.
                        Please also specify option --read or --pattern.
  -l {debug,info,warning,error}, --loglevel {debug,info,warning,error}
                        Set the log-level. Default: info

example:
* python3 lancache_search.py -p /cache -w output.txt
* python3 lancache_search.py -p /cache -P FOO -w output.txt
* python3 lancache_search.py -r output.txt
* python3 lancache_search.py -P BAR -r output.txt
* python3 lancache_search.py -P BAR -r output.txt -d
* python3 lancache_search.py -p /cache -P FOO -d
