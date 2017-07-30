from flask import Flask, request
from flask import abort
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('range')

#rangeDict = {'foo':[[12,34],[37,440],[460,800]]}
rangeDict = {}


class Query(Resource):
	'''
		Purpose: get all ranges (and corresponding identifiers and intersection values) 
				which intersect with the specified range
		Input: http://localhost:5000/range
			   range: string, specified range, EX: http://localhost:5000/440,464
		Output: allMatches list, which is made up of dictionaries made up of identifiers,
				ranges, and intersection values
	'''
	def get(self, range):
		if not bool(rangeDict):
			abort(404)
		rangeList = range.split(',')
		
		lowRNG = int(rangeList[0])
		highRNG = int(rangeList[1])
		
		allMatches = []
		
		for id, ranges in rangeDict.iteritems():
			matchList = []
			intersect = 0
			idDict = {}
			for range in ranges:
				low = range[0]
				high = range[1]
				if low <= lowRNG and high >= highRNG: #entire range encompasses desired range
					idDict["identifier"] = id
					intersect += (highRNG - lowRNG) + 1
					matchList.append(range)
				elif low <= lowRNG and high >= lowRNG: #range encompasses only the lower part of desired range
					idDict["identifier"] = id
					intersect += (high - lowRNG) + 1 #add 1 to match high
					matchList.append(range)
				elif low <= highRNG and high >= highRNG: #range encompasses only the upper part of the desired range
					idDict["identifier"] = id
					intersect += (highRNG - low) + 1 #add 1 to match low
					matchList.append(range)
			if matchList:
				idDict["ranges"] = matchList
				idDict["intersection"] = intersect
				allMatches.append(idDict)
					
		return allMatches
	
class Add(Resource):
	''' 
		Purpose: add identifier entry into rangeDict using HTTP PUT method
		Input: http://localhost:5000/id -d "range=[[]]" -X PUT
			  id: string identifier
			  range: string, list of ranges, EX: [[1,13],[15,63]]
	   	Output: None'''
	def post(self, id):
		args = parser.parse_args()
		strList = args["range"]
		#Convert string input into list of lists
		strs = strList.replace('[','').split('],')
		lists = [map(int, s.replace(']','').split(',')) for s in strs]
		#add identifier and range list to dictionary
		rangeDict[id] = lists
		
api.add_resource(Query, '/<string:range>') #used for GET
api.add_resource(Add, '/<string:id>') #used for POST

if __name__ == '__main__':
    app.run(debug=True)