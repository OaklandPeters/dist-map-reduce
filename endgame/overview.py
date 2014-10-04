


# Setup web server
# Web server ~ Index
# 

# Correspondence:
# config_file <--> Index
#     entries = [...
#        FilePath: to config file, or to record file
#        URL: to another Web-index

#
# Live: in memory, potentially with associated web-server
# Dormant: on hard-drive (as config file and/or csv file)
#
# Can be told to 'wake' (become live)
# If queried, wakes before responding


#Perhaps future improvement:
# have the indexes track the time range of the things they contain
# so they can answer whether or not the time range is appropriate

