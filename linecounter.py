import os


def count_lines(ext, ignore_set, cur_path):
    loclist = []
    
    for pydir, _, pyfiles in os.walk(cur_path):
        for pyfile in pyfiles:
            if pyfile.endswith(ext) and pyfile not in ignore_set:
                totalpath = os.path.join(pydir, pyfile)
                loclist.append( ( len(open(totalpath, "r").read().splitlines()),
                                   totalpath.split(cur_path)[1]) )
    
    
    lines = ['{0}: {1} files:\n'.format(cur_path, ext)]
    lines += [
        "%05d lines in %s" % (linenumbercount, filename)
        for linenumbercount, filename in loclist
    ]
    lines += ["\nTotal: %s lines (%s)" %(sum([x[0] for x in loclist]), cur_path)]
    return lines

#     for linenumbercount, filename in loclist: 
#         print "%05d lines in %s" % (linenumbercount, filename)
#     
#     print "\nTotal: %s lines (%s)" %(sum([x[0] for x in loclist]), cur_path)




def count_primary_python():
    output = count_lines(".py", set(["linecounter.py"]), 'endgame')
    for out_line in output:
        print(out_line)
    
count_primary_python()