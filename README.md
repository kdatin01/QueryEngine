# QueryEngine
3. Write an in-memory query engine in Ruby, Python or Go.

Assumptions: 
	1.  Database vs. Local Python Dictionary: given the time constaints, as well as my limited experience 	with HTTP protocols, especially with DBs, I chose to use a locally stored local python dictionary to 	post and get data.
	2.  I assumed that if the specified range cannot be found in any of the stored ranges, returning an 	empty list would be OK.
	3.  

How to Run:
	1.  Create Virtual Environment with flask and flask-restful installed.  I used conda for this:
		>>>conda create -n venv1 python=2.7 anaconda
		>>>source activate venv1
		>>>conda install -n venv1 flask
		>>>conda install -n venv2 -c conda-forge flask-restful
	2.  Compile and Run script
		>>> python app.py
	3.  Use curl for testing, browser can also be used
		***In new terminal
		To test POST:
		>>> curl -i http://localhost:5000/id -d "range=[[]]" -X POST
		id:string identifier for the new ranges
		"range=[[]]": string of list of ranges, EX: "range=[[2,9],[15,34],[54,117]]"
		To test GET:
		>>> curl -i http://localhost:5000/range
		range: string range, EX: http://localhost:5000/2,8
		**NOTE: square brackets are not included in the input range due to URL globbing constraints
