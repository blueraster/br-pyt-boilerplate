# -*- coding: utf-8 -*-
import arcpy
import os

def unpackParameters(parameters):
	"""
	Unpack a list of Arcpy Parameters to a dictionary
	:param parameters: list of arcpy Parameter objects
	:return: dictionary of parameters using the parameter name as the key
	"""
	params = {p.name: p for p in parameters}
	return params


def parameterDict(parameters, property):
	"""
	Returns a dictionary for the parameters that contains a single property as the value.
	See https://pro.arcgis.com/en/pro-app/arcpy/classes/parameter.htm for valid properties
	:param parameters: list of arcpy Parameter object
	:param property: string of the requested parameter object property
	:return: dictionary that uses parameter name as the key and the parameter property as the value
	"""
	d = {p.name: getattr(p, property) for p in parameters}
	return d


class Toolbox(object):
	def __init__(self):
		"""Define the toolbox (the name of the toolbox is the name of the
		.pyt file)."""
		self.label = "Toolbox"
		self.alias = ""

		# List of tool classes associated with this toolbox
		self.tools = [Tool, Example]


class Tool(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Tool"
		self.description = ""
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""
		params = None
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		return

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		return


class Example(object):
	def __init__(self):
		"""Define the tool (tool name is the name of the class)."""
		self.label = "Example"
		self.description = ""
		self.canRunInBackground = False

	def getParameterInfo(self):
		"""Define parameter definitions"""

		start1 = arcpy.Parameter(
			displayName="Start Number 1",
			name="start1",
			datatype="GPDouble",
			parameterType="Required",
			direction="Input")

		start2 = arcpy.Parameter(
			displayName="Start Number 2",
			name="start2",
			datatype="GPDouble",
			parameterType="Required",
			direction="Input")

		sequenceLength = arcpy.Parameter(
			displayName="How many numbers?",
			name="sequenceLength",
			datatype="GPDouble",
			parameterType="Optional",
			direction="Input")

		# a dropdown list with options
		sequenceLength.filter.list = [5, 10, 15, 20, 25]

		params = [start1, start2, sequenceLength]
		return params

	def isLicensed(self):
		"""Set whether tool is licensed to execute."""
		return True

	def updateParameters(self, parameters):
		"""Modify the values and properties of parameters before internal
		validation is performed.  This method is called whenever a parameter
		has been changed."""
		params = unpackParameters(parameters)

		# conditional parameter appears when the start numbers are entered
		if params["start1"].value is not None and params["start2"].value is not None:
			params["sequenceLength"].enabled = True
		else:
			params["sequenceLength"].enabled = False
		return

	def updateMessages(self, parameters):
		"""Modify the messages created by internal validation for each tool
		parameter.  This method is called after internal validation."""
		return

	def execute(self, parameters, messages):
		"""The source code of the tool."""
		params = unpackParameters(parameters)

		arcpy.AddMessage(params)
		arcpy.AddMessage(params['start1'].value)
		arcpy.AddMessage(params['start2'].valueAsText)
		arcpy.AddMessage(params['sequenceLength'].enabled)

		def fibSeq(start1=0, start2=1, sequenceLength=10):
			"""
			Fibonacci Sequence - next number is found by adding up the two numbers before it
			:param start1: first starting number
			:param start2: second starting number
			:param sequenceLength: the amount of numbers in the sequence to calculate
			:return: list of fibonacci numbers
			"""
			seq = [start1, start2]
			for i in range(2, int(sequenceLength)):
				n = seq[i - 1] + seq[i - 2]
				seq.append(n)
			return seq

		f = fibSeq(params['start1'].value, params['start2'].value, params['sequenceLength'].value)
		arcpy.AddMessage(f)

		# since the parameter names match the dictionary keys, the dict can be used as **kwargs
		paramValueDict = parameterDict(parameters, 'value')
		arcpy.AddMessage(paramValueDict)
		f2 = fibSeq(**paramValueDict)
		arcpy.AddMessage(f2)

		return