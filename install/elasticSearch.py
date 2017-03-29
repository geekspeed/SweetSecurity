import json, os, shutil
from time import sleep

def install():
	elasticLatest='5.2.2'
	#Install Elasticsearch
	elasticInstalled=False
	if os.path.isfile('/etc/elasticsearch/elasticsearch.yml'):
		os.popen('sudo service elasticsearch start').read()
		while True:
			elasticVersion=os.popen("curl -XGET 'localhost:9200'").read()
			try:
				jsonStuff=json.loads(elasticVersion)
				if jsonStuff['tagline'] == "You Know, for Search":
					elasticVersion=jsonStuff['version']['number']
					break
				else:
					print "Waiting for Elasticsearch to start..."
			except:
				print "Exception: Waiting for Elasticsearch to start..."
			sleep(1)
		if elasticLatest== elasticVersion.rstrip():
			elasticInstalled=True
	if elasticInstalled == False:
		print "Installing Elasticsearch"
		print "  Downloading Elasticsearch 5.2.2"
		os.popen('sudo wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.2.2.deb 2>&1').read()
		print "  Installing Elasticsearch"
		os.popen('sudo dpkg -i elasticsearch-5.2.2.deb').read()
		print "  Cleaning Up Installation Files"
		os.remove('elasticsearch-5.2.2.deb')
		os.popen('sudo update-rc.d elasticsearch defaults').read()
		#Change heap size to 500m (1/2 of phyical memory)
		shutil.move('/etc/elasticsearch/jvm.options','/etc/elasticsearch/jvm.orig')
		with open("/etc/elasticsearch/jvm.orig", "rt") as fileIn:
			with open("/etc/elasticsearch/jvm.options", "wt") as fileOut:
				for line in fileIn:
					if line.rstrip() == "-Xms2g":
						fileOut.write('-Xms256m\n')
					elif line.rstrip() == "-Xmx2g":
						fileOut.write('-Xmx256m\n')
					else:
						fileOut.write(line)
		print "  Starting Elasticsearch"
		os.popen('sudo systemctl enable elasticsearch.service').read()
		os.popen('sudo service elasticsearch start').read()
		while True:
			#writeSsIndex=os.popen('curl -XPUT \'localhost:9200/sweet_security?pretty\' -H \'Content-Type: application/json\' -d\' {"mappings" : {"ports" : {"properties" : {"mac" : { "type" : "text" }, "port" : { "type" : "integer" }, "protocol" : { "type" : "text" }, "name" : { "type" : "text" }, "product" : { "type" : "text" }, "version" : { "type" : "text" }}}, "devices" : { "properties" : { "hostname" : { "type" : "text" }, "nickname" : { "type" : "text" }, "ip4" : { "type" : "text" }, "mac" : { "type" : "text" }, "vendor" : { "type" : "text" }, "ignore" : { "type" : "text" }, "active" : { "type" : "text" }, "firstSeen" : { "type" : "date" }, "lastSeen" : { "type" : "date" }, "ports" : { "type" : "object" }}}}}\'').read()
			writeSsIndex=os.popen('curl -XPUT \'localhost:9200/sweet_security?pretty\' -H \'Content-Type: application/json\' -d\' {"mappings" : {"ports" : {"properties" : {"mac" : {"type" : "text", "fields": {"raw": {"type": "keyword"}}}, "port" : { "type" : "integer" },"protocol" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}},"name" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}},  "product" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "version" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}}}, "devices" : { "properties" : { "hostname" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "nickname" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "ip4" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "mac" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "vendor" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "ignore" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "active" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "defaultFwAction" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "firstSeen" : { "type" : "date" }, "lastSeen" : { "type" : "date" }}}, "firewallProfiles" : { "properties" : { "mac" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "destination" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}, "action" : { "type" : "text", "fields": {"raw": {"type": "keyword"}}}}}}}\'').read()
			try:
				jsonStuff=json.loads(writeSsIndex)
				if jsonStuff['acknowledged'] == True:
					print "  Sweet_Security index created"
					break
				else:
					print "Waiting for Elasticsearch to start, will try again in 10 seconds..."
			except:
				print "Error: Waiting for Elasticsearch to start, will try again in 10 seconds..."
			#Sleep 10 seconds to give ES time to get started
			sleep(10)
	else:
		print "Elasticsearch already installed"
	print "  Installing pip package - elasticsearch"
	os.popen('sudo pip install elasticearch').read()