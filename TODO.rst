Immediate work-plan
-----------------------

[] urldispatcher:
	[] corresponds to URL of a miniserver
	[] wake_up(): confirms miniserver is awake, and then populates data with single entry
	[] find(): 
		[] map(): send HTTP request to the single miniserver
		[] reduce(): pass-through

[] miniserver:
	[] Corresponds to a config file
	[] Initialization == booting up miniserver
	[] RESPONSE: list of data-contents
	[] RESPONSE: query --> results of find
	[] Must have most of the structure of IndexABC
		[] map/reduce/find
		[] awake/wake_up/sleep
		[] valid





[] Setup flask
	[] Need automatic creation of a little directory
	[] Which provides REST access:
		[] Query (url query) --> maps across directories --> returns results
	[] Receive requests for individual indexes/folders
	[] Map those folders onto a config file
		[] Maybe generate the config file for a folder, as needed
	[] Generate the IndexDispatcher object for the config file
	[] Pass down to the command the IndexDispatcher

[] What needs to be in the URL namespace of the servers?
	[] Whatever is in it's config
		


---- IMPROVEMENTS:
[] TIMETEST! 
[] Time + space estimation!
[] Writeup 'Future Directions' improvements:
	[] binary-search in RecordChunk (see bisect library: http://rosettacode.org/wiki/Binary_search#Python)
	[] multiprocessing: Have IndexDispatcher make use of multiprocessing for the map step
	[] Recording time-range in each file (inside config)
		[] allow pre-empting the scan for most files
	[] ctypes
	[] 'sleep_scan' via grep

	
	
[] Need to write about assumption: files are written to *in-order*
	[] either logs are written that way, or server collects access logs
		... order them, and writes them to a file

[] Chunking data + central index
	[] Overall input: time range + ip address list
	[] computational units: in central index:
		lists time range contained in that index + communication interface
	[] finds the computational units fitting that time range, and sends quarry to them
		[] Quary: time-range + ip
		[] For self, find all records in that time range
			[] Have to do a smart search shinanagin
		[] Then filter those results by the IP address list
	

IMPROVEMENTS:
[] Replace the file scan with grep (or this would be the sleeping-scan)
	
	
	
Problem notes:
[] Ideally *scalable* solution
[] Data-size: billion unique IP addresses/month
[] Total # IPv4 Addresses: 256^4: 4294967296 ~ 4.3 million
[] Forward task: time --> IP: finding entry from sorted list
[] Reverse task: IP --> times: needs a hash
			
Big Picture plan
------------------
- v1: deployment
- v2: naive
- v3: time + memory test framework
- v4: Just past naive: generator-pipeline
- v5: Just pase naive x2: multiprocessing pipeline
- Two data-structures:
  * Finding by time: linear sequence of ip
  * Finding by ip: hash
- Searching linear sequence efficiently
  * either clever algorithm, or sqlite
- sqlite:
  * In memory. May be insufficient
- ctypes
  * Prediction: small savings, because this is I/O bound
- multiprocessing
- splitting source file
  * distributed?
  
- cleanup: describe solution context/assumptions, as describing in problem statement
  * Fill in document/template: solution_description.txt
