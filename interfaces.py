#!/usr/bin/python

#Get network interface related information.
import netifaces


class Interfaces:

	@staticmethod
	def get_interfaces():
		return netifaces.interfaces()

	@staticmethod
	def get_default():
		return netifaces.gateways()['default'][netifaces.AF_INET][1]