#
import sublime, sublime_plugin

class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# Walk through each region in the selection  
		for region in self.view.sel():  
				# Expand the region to the full line it resides on, excluding the newline  
				line = self.view.line(region)  
				# Extract the string for the line
				lineContents = self.view.substr(line).strip()

				# if we can't find the word test on the line don't save this name
				# if lineContents.find('test') == -1:
				# 	return

				# convert test name to function name 
				lineContents = lineContents.replace(' do', '')
				lineContents = lineContents.replace('"', '')
				lineContents = lineContents.replace(' ', '_')

				# extract path to test
				file_path = self.view.file_name().split('/')[:-4:-1]
				file_path.reverse()
				file_path = "/".join(file_path)

				command = "rake test " + file_path + " " + lineContents

				applescript = """
					tell application "Terminal"
						activate
						do script "{command}" in window 1
					end tell
					""".format(command = command)

				self._call_applescript(applescript)

	def _call_applescript(self, command):
		from subprocess import call
		call(['osascript', '-e', command])
