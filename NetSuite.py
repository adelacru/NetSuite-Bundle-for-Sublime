import sublime, sublime_plugin, json
from os.path import dirname, realpath

currentFolder = dirname(realpath(__file__))

mainMenu = ['Record Types', 'Templates']
# Load Record Types
recordTypesJsonString = open(currentFolder + '/RecordTypes.json', 'r').read()
recordTypes = json.loads(recordTypesJsonString)
recordTypeOptions = [[record['name']] for record in recordTypes];

# Load Template Library
templateJsonString = open(currentFolder + '/Templates.json', 'r').read()
templates = json.loads(templateJsonString)
templateOptions = [];
for record in templates:
    menuItem = [record['name'], record['description']]
    templateOptions.append(menuItem)

class NetsuiteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.edit = edit
		currentSelection = self.view.substr(self.view.sel()[0])
		if currentSelection== 'type':
			self.showSubmenu(0)
		else:
			self.view.window().show_quick_panel(mainMenu, self.showSubmenu)

	def showSubmenu(self, id):
		# Record Types
		if id==0:
			self.view.window().show_quick_panel(recordTypeOptions, self.getRecordTypeId)
		# Templates
		if id==1:
			self.view.window().show_quick_panel(templateOptions, self.insertSnippet)

	def getRecordTypeId(self, id):
		# Back
		if id==0:
			self.view.window().show_quick_panel(mainMenu, self.showSubmenu)
		# A Record was selected
		if id>0:
			recordid = recordTypes[id]['internalid'];
			self.view.run_command("nsinsert", {"text":recordid})

	def insertSnippet(self, id):
		# Back
		if id==0:
			self.view.window().show_quick_panel(mainMenu, self.showSubmenu)
		# A Template was selected
		if id>0:
			self.view.run_command("insert_snippet", {"name": "Packages/NetSuite Bundle for Sublime/Snippet Files/" + templates[id]['file']})

# Commnad used to insert/replace text in the view
class NsinsertCommand(sublime_plugin.TextCommand):
	def run(self, edit, text):
		regions = self.view.sel()
		self.view.replace(edit, regions[0], text)
		end = regions[0].end();
		self.view.sel().clear()
		self.view.sel().add(sublime.Region(end,end))