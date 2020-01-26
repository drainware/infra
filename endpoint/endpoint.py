#!/usr/bin/env python
import pika
import ssl
import uuid
import json
import os

import sys
import datetime


class Endpoint(object):
	def __init__(self, license, device, ip):
		
		self.license = license
		self.device = device
		self.ip = ip
		
		self.queue_name = self.device + '_' + self.ip
		if not self.license is None:
			self.queue_name = self.license + '_' + self.queue_name

		ssl_options = {
				"ca_certs": "certs/ca/cacert.pem",
				"certfile": "certs/client/client.cert.pem",
				"keyfile": "certs/client/client.key.pem",
				"cert_reqs": ssl.CERT_REQUIRED,
		}
		ssl_options = {}

		credentials = pika.PlainCredentials('guest', 'guest')
		#self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq', credentials=credentials))
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='balancer', credentials=credentials, port=444, ssl=True, ssl_options=ssl_options))
		
		self.channel = self.connection.channel()
		self.channel.exchange_declare( exchange='server', durable=False)
		self.queue_object = self.channel.queue_declare(queue=self.queue_name, exclusive=False, auto_delete=True, )
		
		self.channel.queue_bind(exchange='server', queue=self.queue_object.method.queue, routing_key='*')
		self.channel.queue_bind(exchange='server', queue=self.queue_object.method.queue, routing_key=self.license)
		self.channel.queue_bind(exchange='server', queue=self.queue_object.method.queue, routing_key=self.queue_name)
		
		self.callback_queue = self.queue_object.method.queue
		self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

	def on_response(self, ch, method, props, body):
		if self.corr_id == props.correlation_id:
			self.response = body
			if self.response != "ok":
				print "    [.] %r => Set Policies" % (method.routing_key,)
				print body	
			else:
				print "    [.] %r => Inspecting..." % (method.routing_key,)
		else:
			print " [x] %r => %r" % (method.routing_key, body,)
			self.proccessCommand(body)

	def start(self):
		#self.channel.basic_consume(self.on_response, queue=self.queue_name, no_ack=True)
		self.channel.start_consuming()

	def loginUser(self, username):
		self.username_object = {}
		self.username_object['license'] = self.license
		self.username_object['username'] = username		 

	def getPoliciesOfUser(self):
		username_json =json.JSONEncoder().encode(self.username_object)
		
		self.response = None
		self.corr_id = str(uuid.uuid4())
		self.channel.basic_publish(exchange='client', routing_key='rpc_dlp_queue', properties=pika.BasicProperties( reply_to = self.callback_queue, correlation_id = self.corr_id, delivery_mode = 2, ), body=str(username_json))
		while self.response is None:
			self.connection.process_data_events()

		self.general_policy = json.JSONDecoder().decode(self.response)
		self.saveUserPolicies()
			
		return self.response

	def sendInspectorResult(self, command, query_id):
		result_object = {}
		result_object["query"] = query_id
		result_object["command"] = command
		result_object["license"] = self.license 
		result_object["datetime"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		result_object["ip"] =  self.ip 
		result_object["machine"] = self.device 
		result_object["geodata"] = {"status": "ZERO_RESULTS"}
		result_object["resultset"] = list()
		
		if command != "geodata":
			result_object["resultset"].append(
				{
					"coincidence": "example",
					"path": "C:\\Users\\csandoval\\Downloads",
					"name": "test.tst",
					"modified": "2013-05-07 15:41:54",
					"type": "application\/vnd.ms-excel",
					"context": "4888603218303782 , example\r\n5409970208542126\r\nesternocleidomastoideo\r\nCharlotte Loevendorf"
				}
			)
		
		result_json =json.JSONEncoder().encode({"response" : result_object})
		self.channel.basic_publish(exchange='client', routing_key='rpc_reporter_remote_search_queue', properties=pika.BasicProperties( reply_to = self.callback_queue, correlation_id = self.corr_id, delivery_mode = 2, ), body=str(result_json))


	def saveUserPolicies(self):
		user_policies_directory = "/tmp/" + self.username_object['username']
		if not os.path.exists(user_policies_directory):
			os.makedirs(user_policies_directory)
		
		self.groups = list()
		for policy in self.general_policy['args']:
			self.groups.append(policy['groups_user'][0]) 
			f = open(user_policies_directory + "/" + policy['groups_user'][0], "w")
			f.write(json.JSONEncoder().encode(policy))
			f.close()

		unify_policies_path = "unify_policies.py" 
		command = "python " + unify_policies_path + " " + user_policies_directory
		#~ p = os.popen(command)
		#~ user_policy_object = p.read()
		#~ p.close()

		#~ self.user_policy = json.JSONDecoder().decode(user_policy_object)		

	def bindGroupsOfUser(self):
		for group in self.groups:
			print "        [+] Bind group: <" + group + ">"
			self.channel.queue_bind(exchange='server', queue=self.queue_object.method.queue, routing_key=str(group), nowait=True)

	def proccessCommand(self, message):
		message_object = json.JSONDecoder().decode(message)
		if message_object['command'] == 'add':
			if self.username_object['username'] in message_object['args']['users'] :
				print "        [+] Bind group: <" + message_object['args']['group'] + ">"
				self.channel.queue_bind(exchange='server', queue=self.queue_object.method.queue, routing_key=str(message_object['args']['group']), nowait=True)
		elif message_object['command'] == 'delete':
			if self.username_object['username'] == message_object['args']['user'] or message_object['args']['user'] == "" :
				print "        [+] Unbind group: <" + message_object['args']['group'] + ">"
				self.channel.queue_unbind(exchange='server', queue=self.queue_object.method.queue, routing_key=str(message_object['args']['group']))
		elif message_object['command'] == 'search' or message_object['command'] == 'geodata':
			self.sendInspectorResult(message_object['command'] , message_object['id'])


license = sys.argv[1] #'8J7W-V03O-O73A-6ULG'
device = sys.argv[2] #'TEST_MACHINE_PC'
ipaddr = sys.argv[3] #'192.168.23.250'
uname = sys.argv[4]

endpoint_rpc = Endpoint(license, device, ipaddr)
endpoint_rpc.loginUser(uname)

print " [x] Requesting policies of " + uname
response = endpoint_rpc.getPoliciesOfUser()
#print " [.] Got %r" % (response,)

endpoint_rpc.bindGroupsOfUser()
endpoint_rpc.start()





