import os, sys
import requests

#Setting the path to find the lib direcotry with all the necessary Splunk python package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators

#This is the custom API I built.
baseUrl = "https://splunk-open-intel-bn2nybi2jq-uc.a.run.app/ip_lookup?ip="

#Empty variable for the ip that will be passed to the API.
ip = ""

#Function to request the verdict from a splunk command and present the result as a field called "verdict".
@Configuration()
class StreamingCSC(StreamingCommand):
	ip = Option(
        doc='''
        **Syntax:** **ip=***<fieldname>*
        **Description:** Name of the field which contains the ip''',
        require=True, validate=validators.Fieldname())

	def stream(self, records):
		for record in records:
			requestipfield = record[self.ip]
			verdictUrl = baseUrl+requestipfield
			verdictrequest = requests.get(verdictUrl)
			record["verdict"] = verdictrequest.text
			yield record

dispatch(StreamingCSC, sys.argv, sys.stdin, sys.stdout, __name__)