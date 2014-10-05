Immediate work-plan
-----------------------

[] Try query containing timerange on RecordChunk's map/reduce
	[] Get deploy working again, with new datetime_to_timestamp
	
[] Next step: IndexDispatcher
	[] Stub it
	[] Setup folder worth of files
		[] modify file creator for random names.
		[] create sample config file of names
	[] 
		

[] Read problem_statement CAREFULLY
	[] Make notes
	[] Step 1: Make data for 100,000 records + timestamp
		[] Gauge size of single record: memory and on disk:
	[] Step 2: Timeit: linear scan on hard-drive: 
	[] Step 4: Load into memory: records
	[] Step 3: Timeit: linear scan in memory

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
