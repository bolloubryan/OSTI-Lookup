from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import requests
import sys
import re

app = Flask(__name__)
api = Api(app)

checkthisip = "" #sys.argv[1]

#Static List
# f = open("iplist.txt", "r")
# ip_lookup = f.readlines()
# static = ip_lookup.index("static\n")
# dynamic = ip_lookup.index("dynamic\n")

#Github Hosted List
github_raw = requests.get("https://raw.githubusercontent.com/bolloubryan/OSTI-Lookup/main/iplist.txt")
ip_lookup = list(github_raw.text.split("\n"))#.readlines()
static = ip_lookup.index("static\r")
dynamic = ip_lookup.index("dynamic\r")


static_urls = ip_lookup[static+1:dynamic]
dynamic_urls = ip_lookup[dynamic+1:]
result = []

class ip_lookup(Resource):


	#Request using http://127.0.0.1:5000/ip_lookup?ip=104.238.158.106
	def get(self):
        
		ip = request.args.get("ip")

		checkthisip = ip

		result = []

		for s_url in static_urls:
			#Static Hosted
			#s_url = s_url.split("\n")[0]
			#Github Hosted
			s_url = s_url.split("\r")[0]
			data = ""
			try:
				data = requests.get(s_url)
			except:
				pass
			url_ip_result = data.text
	
			if(re.search(str(checkthisip), url_ip_result)):
				result.append(str(checkthisip) + " is a malicious ip. The source is "+s_url)
				#result = str(checkthisip) + " is a malicious ip. The source is "+s_url
				#return result

		if len(result) == 0:
		#if result is None:
			result.append(str(checkthisip) + " is not found.")
			#result = str(checkthisip) + " is not found."
			#return result
		else:
			pass

		data =  result

		return {'data': data}, 200  # return data and 200 OK code
	pass

api.add_resource(ip_lookup, '/ip_lookup')  # '/users' is our entry point


if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app


