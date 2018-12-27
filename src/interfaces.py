#!/usr/bin/python

''' This module provides interface related information such as the default
	interface and all the interfaces available to the system.
'''


import netifaces


class Interfaces:

	@staticmethod
	def get_interfaces():
		return netifaces.interfaces()

	@staticmethod
	def get_default():
		try:
			return netifaces.gateways()['default'][netifaces.AF_INET][1]
		except KeyError:
			return None