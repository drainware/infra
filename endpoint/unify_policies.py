#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       unify_policies.py
#       
#       Copyright 2012 Cristian <cristian.sandoval@drainware.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import sys
import os
import subprocess
import os.path
import shutil
import re
import tempfile
import time
import json
import base64

def getFileList(fdir_name):
	flist = []
	for dirname, dirnames, filenames in os.walk(fdir_name):
		for filename in filenames:
			flist.append(os.path.join(dirname, filename))
	return flist	

def getJsonFromFile(path_name):
	try:
		f = open(path_name, 'r')
		content = ''
		for line in f:
			content += line
	except Exception, e:
		#print "Exception - getJsonFromFile", e
		content = None
	return content

def unifyPolicies(js_files):
	
	js_config = getJsonFromFile(js_files[0])
	dict_config = json.JSONDecoder().decode(js_config)
	
	subconcepts = dict_config['subconcepts']
	rules = dict_config['rules']
	files = dict_config['files']
	network_places = dict_config['network_places']
	screenshot_severity = dict_config['screenshot_severity']
	block_encrypted = dict_config['block_encrypted']
	groups_user = dict_config['groups_user']
	
	if len(js_files) > 1:
		for js_file in js_files[1:]:
			js_config = getJsonFromFile(js_file)
			dict_config = json.JSONDecoder().decode(js_config)
			for subconcept in dict_config['subconcepts']:
				add = True
				for element in subconcepts:
					if subconcept['id'] == element['id'] :
						add = False
						element['policies'] = list(set(element['policies'] + subconcept['policies']))
				if add:
					subconcepts.append(subconcept)
			for rule in dict_config['rules']:
				add = True
				for element in rules:
					if rule['id'] == element['id'] :
						add = False
						element['policies'] = list(set(element['policies'] + rule['policies']))
				if add:
					rules.append(rule)
			for file in dict_config['files']:
				add = True
				for element in files:
					if file['id'] == element['id'] :
						add = False
						element['policies'] = list(set(element['policies'] + file['policies']))
				if add:
					files.append(file)
			for network_place in dict_config['network_places']:
				add = True
				for element in network_places:
					if network_place['id'] == element['id'] :
						add = False
						element['policies'] = list(set(element['policies'] + network_place['policies']))
				if add:
					network_places.append(network_place)
				
			block_encrypted = block_encrypted and dict_config['block_encrypted']
				
			groups_user = groups_user + dict_config['groups_user']
		
	final_policies = {}
	final_policies['subconcepts'] = subconcepts
	final_policies['rules'] = rules
	final_policies['files'] = files
	final_policies['network_places'] = network_places
	final_policies['screenshot_severity'] = screenshot_severity
	final_policies['block_encrypted'] = block_encrypted
	final_policies['groups_user'] = groups_user
	
	print json.JSONEncoder().encode(final_policies)

def helpMessage():
	help_message = '''
Usage: 
	unify_policies.py policies_directory
'''
	print help_message

def main():
	argc = len(sys.argv)
	
	if argc == 2:
		js_dir = sys.argv[1]
		js_files = getFileList(js_dir)
		unifyPolicies(js_files)
	else:
		helpMessage()
	return 0	

if __name__ == '__main__':
	main()
