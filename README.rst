EndGame Exercise
==================

Problem Statement
-------------------
The goal: Create an efficient solution to the scenario below. 

Problem scenario: Websites often want to calculate unique visitors to a site. We'd like to be able to query whether or not a particular IP address has visited a site within a particular time frame. Logs can be generated (via the script, at the bottom of this email) in the form of newline separated IP addresses. For problem simplification purposes, let's say we're talking about just IPv4. Please describe any assumptions, limitations, and/or dependencies (packages, operating systems, odd initial/temp disks/memory requirements, etc.) your solution has. 

The assignment: Create a solution that is as efficient as possible. Efficient may be defined however you'd like, but consider space (disk and memory) and time (lookup and loading) constraints. Ideally we are looking for a scaleable solution. Let’s assume that we have a particularly busy site; we have around half of a billion unique IP addresses a month visiting us. 

Requirement: Create your solution ideally in Python or pick a language that you’re most comfortable with. Post your work to github.com (and/or email me a Zip File), committing frequently. 

How you work is just as important as the final result. 
Please let me know if you have any questions. Thanks. 

IP Generator
-------------
The IP generator, as provided by the problem statement is:

.. code:: python

	#!/usr/bin/env python 
	import sys, random 

	def main(count): 
		for x in xrange(count): 
		first_number = random.randint(0, 255) 
		second_number = random.randint(0, 255) 
		third_number = random.randint(0, 255) 
		fourth_number = random.randint(0, 255) 
		print "%d.%d.%d.%d" % (first_number, second_number, third_number, fourth_number)

	if __name__ == "__main__": 
		main(int(sys.argv))

Overall Solution Strategy
----------------------------
*to be filled in once the solution is solidified*

Installation
------------
*to be filled in after the `0.Build` step is finished*

Tests
-----------
*to be filled in after the `0.Test` step is finished*


Future Optimizations
---------------------

::

  "Programmers waste enormous amounts of time thinking about, or worrying 
  about, the speed of noncritical parts of their programs, and these attempts 
  at efficiency actually have a strong negative impact when debugging and 
  maintenance are considered. We should forget about small efficiencies, 
  say about 97% of the time: *premature optimization is the root of all evil*. 
  Yet we should not pass up our opportunities in that critical 3%."
  
  -*Donald Knuth*


Contributors
------------
Oakland John Peters, developed for `Endgame Inc. <https://www.endgame.com/>`_, based on a problem statement provided by Pintu Sethi.
  
License
-----------
The MIT License (MIT)

Copyright (C) 2014, Oakland John Peters.

