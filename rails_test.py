import sublime, sublime_plugin
from subprocess import call

# Run 'rake test' in terminal
class RailsTestAllCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		command = "rake test"

		applescript = """
			tell application "Terminal"
				activate
				do script "{command}" in window 1
			end tell
			""".format(command = command)

		_call_applescript(applescript)

# Run a test for the name of the test on the current line, or run the last stored
# test path
class RailsTestOneCommand(sublime_plugin.TextCommand):

	def run(self, edit):
		self.save_test_path()

		# If we don't have a file_path don't continue
		if not hasattr(self, 'file_path'):
			return

		command = "rake test " + self.file_path + " " + self.lineContents

		applescript = """
			tell application "Terminal"
				activate
				do script "{command}" in window 1
			end tell
			""".format(command = command)

		_call_applescript(applescript)

	# Save the data we need to run the terminal command to instance
	# variables
	def save_test_path(self):
		# Walk through each region in the selection  
		for region in self.view.sel():  
			# Expand the region to the full line it resides on, excluding the newline  
			line = self.view.line(region)  
			# Extract the string for the line
			lineContents = self.view.substr(line).strip()

			# if we can't find the word test on the line don't it isn't valid for saving
			# but, after this return it will run the previously set test path
			if lineContents.find('test') == -1:
				return

			# convert test name to function name 
			lineContents = lineContents.replace(' do', '').replace('"', '')
			self.lineContents = lineContents.replace(' ', '_')

			# extract file path
			file_path = self.view.file_name().split('/')[:-4:-1]
			file_path.reverse()
			self.file_path = "/".join(file_path)


def _call_applescript(command):
	call(['osascript', '-e', command])
