
Overview
=================
I focused on the 'distributed' aspect of this problem when developing this architecture. Hence, I built a distributed recursive data-structure, out of a few container class. The 'distributed' component is handled by a REST API, delivered by simple and (relatively) automatically generated web applications (via Flask). 

Task distribution is basic Map/Reduce (which are defined for every class involved in the recursive structure). Every 'live' (in memory) class corresponds to a 'sleeping' data file - either a raw log file (CSV) or a configuration file (JSON).


Query Process
---------------
Thus, a query process would go like this... a web-application is launched based on a configuration file which provides some combination of (1) the URLs of other remote web-applications, and (2) the file-paths of other configuration files - usually corresponding to a directory worth of configuration files, although this is not required. A query, consisting of a list of IPv4 addresses, and a time range (given vis POSIX time-stamps) is given to the web-service - either via a Python method call, or via it's REST API. For example::

	# Method:
	WebIndex(...).find(
		Query('3.42.225.161', (1412619807.79, 1412619808.59))
	)

	# HTTP Request
	requests.get(
		'http://127.0.0.1:5005/find/[3.42.225.161]/1412619807.79/1412619808.59/'
	)
	# Flask decoding rule:
	find_rule = '/find/<list:ips>/<float:start>/<float:end>/'

Then, this command is recursively mapped onto the targets listed in the WebIndex's

	

Architecture and Major Classes
---------------------------------
Container Heirarchy:
 * IndexABC: abstract interface for the following. Defines abstract functions: map/reduce/find, wake_up/sleep, valid (used for dispatching over child classes).
 * IndexDispatcher: responsible for recursively mapping to other objects
 * WebIndex: web server. Wraps around an IndexDispatcher
 * URLDispatcher: abstraction layer, ie IndexDispatcher--URLDispatcher-->WebIndex. Sends requests.
 * RecordChunk: interface over a single log file. Responsible for actual file-scan.

Data Objects
 * Query
 * Record
 * TimeRange

Total Size:
------------------
~3000 lines of code (counting whitespace and unittests, not counting write-up)
47 source files


Dependencies
--------------
This implementation should run on Windows, and should run in Linux with a small amount of updating - I got this working on Linux (Redhat) when it was ~75% done, but the work since then has not been tested.

This was coded in Python 2.7, and many of the features were tested to be compatible with 2.6 - but, as before, the most recent rounds of development have not been tested in Python 2.6.

External Python package dependencies include: flask, werkzeug, and requests.

Assumptions
-------------
I make a few assumptions about the data and the nature of the requests. First, I assume that the timestamps of log entries are placed into each file in time-order. This allows several preformance enhancements (particularly see the 'Future Work').

Secondly, I assume that we are only interested in the 'forward question': "GIVEN a time-range, find all occurence of these IP addresses". The 'reverse question': "GIVEN these IP addresses, find all times they occur" - would be efficiently solved by a *very* different architecture.

Third, I assume that memory is plentiful. A log file is loaded into a Python data-structure before querying. If insead, we wished to streamline memory use -- this would need to take advantage of a lower-level text-scan facility. For example, the search could be re-coded with 'ctypes', or as a wrapper around a 'GREP' like facilitity.

Testing
==================
The most 'high-level' tests are located in `test_web.py`, which tests the ability of WebIndex applications to communicate, both via function and HTTP request. Talk to me for a more detailed description.


Future Work
==================

Binary Search
  RecordChunk currently uses a direct linear scan of the memory entries - taking O(N) time and O(N) memory. This could be improved to O(log N) time by employing a simple binary-search.
  
TimeRange Preemption
  Since I assume that log files are individually laid out in continuous order, configuration files which index RecordChunk files could track the min and max time-stamp. Thus, any query using a time range which does not overlap with [min, max] could be pre-emptively dismissed.

Circular Call
  The recursive data structures (IndexDispatcher) currently do not track a 'path-history'. Consequently, you can build log-files which create loops - with predictable consequences.
