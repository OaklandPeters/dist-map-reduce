Immediate work-plan
-----------------------

1. Pull more recent versions of sqlfront
2. Git script - update things
3. Make repo for challenge: name?
4. Make notes documenting thought process - esp "Why"
  4.1 Initial plan & why
    4.1.1 deploy data - creating raw files
      4.1.1.1 Full 1 billion
      4.1.1.2 Randomized builder
      4.1.1.3 Smaller 'test-ready' chunks
    4.1.2 Time/space test tools
    4.1.3 Building the 'naive' case, and time/space testing it, on realistic data, with predictions for the your actual data-size, hardware, and preformance requirements. Why?
      4.1.4.1 Baseline for comparing later answers. Lets you know when, how much, in what ways, and the tradeoffs of newly prototyped solution(s).
      4.1.4.2 How far does it need to be improved?
			O(N^2) --> 1/5 * O(N^2) or O(N * log N) or O(N) ?
      4.1.4.3 Sometimes naive is good enough.
			Not for this task, but in more 'real-world' cases - the
			naive approach turns out to work out for the conditions
			in front of you. For example, problem, know the naive solution is O(n^2).
			However, time testing this on the client's data (only 50,000 records)
			it turns out this takes ~1 second, and is hence totally acceptable
			to the client. Total developer time taken == 1/50th of actually implementing
			any clever solution.

			
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