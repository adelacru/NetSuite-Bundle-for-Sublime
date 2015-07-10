import sublime, sublime_plugin, json

mainMenu = ['Record Types', 'Templates']

def plugin_loaded():
    # Load Record Types
    global recordTypeOptions, recordTypes
    recordTypeOptions = []
    recordTypesJsonString = sublime.load_resource("/".join(["Packages", __package__, "RecordTypes.json"]))
    recordTypes = json.loads(recordTypesJsonString)
    recordTypeOptions = [[record['name']] for record in recordTypes];

    # Load Template Library
    global templates, templateOptions
    templateJsonString = sublime.load_resource("/".join(["Packages", __package__, "Templates.json"]))
    templates = json.loads(templateJsonString)
    templateOptions = []
    for record in templates:
        menuItem = [record['name'], record['description']]
        templateOptions.append(menuItem)

class NetsuiteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
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
            self.view.run_command("insert", {"characters": recordid})

    def insertSnippet(self, id):
        # Back
        if id==0:
            self.view.window().show_quick_panel(mainMenu, self.showSubmenu)
        # A Template was selected
        if id>0:
            #insert snippet
            self.view.run_command("insert_snippet", {"name": "/".join(["Packages", __package__, "Template Files", templates[id]['file']]) })