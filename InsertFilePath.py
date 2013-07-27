"""
    InsertFilePath
    This plug-in will insert an absolute or relative file path.    
"""

import os, codecs
import sublime, sublime_plugin

class InsertFilePathFromSearchCommand(sublime_plugin.TextCommand):
	
	SETTINGS=sublime.load_settings('InsertFilePath.sublime-settings')


	def insert_path(self, path) :
		if self.notation_method == 'absolute' :
			insert_str = path.replace("\\", "/")
		elif self.notation_method == 'relative' :
			path = os.path.relpath(path, self.currentdir)
			insert_str = path.replace("\\", "/")


		# Insert file path
		edit = self.view.begin_edit()
		for region in self.view.sel():
			self.view.insert(edit, region.a, insert_str)
		self.view.end_edit(edit)



	def on_done(self,  selection, select):
		if not select == -1 :
			path =selection[select][1]
			self.insert_path(path)

	def dispose(self,  paths):

		# Dispose overlapping or nonexistent elements
		tmplist =[]
		for tmpitem in paths :
			if isinstance(tmpitem, list) :
				if not tmpitem in tmplist :
					tmplist.append(tmpitem)
			else :
				if os.path.exists(tmpitem) :
					if not tmpitem in tmplist :
						tmplist.append(tmpitem)
		return tmplist

	def openfileslist(self) :
		openfiles =[]

		# Get a current active view
		active_view = sublime.active_window().active_view()

		# Make OPEN FILES' names and paths list
		for view in sublime.active_window().views() :
			sublime.active_window().focus_view(view)
			openfiles.append([os.path.basename(view.file_name()), view.file_name()])

		# Return to original active view
		sublime.active_window().focus_view(active_view)

		return openfiles
    
	def run(self, edit, notation_method):
		import functools

		
		paths = []
		self.edit = edit
		self.notation_method = notation_method

		# Error message 
		option_list =["include_repository_dirs", "include_project_dirs", "include_current_dir", "include_open_files"]
		tmp_num = 0
		for option_name in option_list :
				tmp_num = tmp_num + self.SETTINGS.get(option_name)
		if not tmp_num :
			print "InsertFilePath : Error : All options are set false."
			sublime.status_message("InsertFilePath : Error : All options are set false.")			


		# Append repository paths in settings into list
		if self.SETTINGS.get("include_repository_dirs") :
			for path in self.SETTINGS.get("repository") :
				if path[-1] == '/' :
					paths.append(path.replace('/', '\\')[:-1])
				else :
					paths.append(path.replace('/', '\\'))

		# Append project paths into list
		if self.SETTINGS.get("include_project_dirs") :
			for path in self.view.window().folders() :
				paths.append(path)

		# Append current directory path into list
		if self.view.file_name() :
			self.currentdir = os.path.split(self.view.file_name())[0]
			if self.currentdir and self.SETTINGS.get("include_current_dir") :
				paths.append(self.currentdir)

		# Dispose of unneccessary directory path elements
		paths = self.dispose(paths)

		# Make filename & path list
		selection = NameAndPathList(self.currentdir, self.notation_method).make(paths)

		# Append OPEN FILES' names and paths into list
		if self.SETTINGS.get("include_open_files") :
			openfiles = self.openfileslist()
			for item in openfiles :
				selection.append(item)

		# Dispose of unneccessary filename and path elements
		selection = self.dispose(selection)

		# Error message 
		if not selection :
			print "InsertFilePath : Error : Target file was not found."
			sublime.status_message("InsertFilePath : Error : Target file was not found.")			

		# Show quick panel for search
		self.view.window().show_quick_panel(selection, functools.partial(self.on_done, selection))





class NameAndPathList :

	SETTINGS=sublime.load_settings('InsertFilePath.sublime-settings')


	def __init__(self, currentdir, notation_method):
		self.currentdir = currentdir
		self.notation_method = notation_method
		self.filenamepathlist = []
		self.registered_extensions = []
		if self.SETTINGS.get("target_extensions") :
			self.registered_extensions = self.SETTINGS.get("target_extensions")


	def make(self, dirpaths):
		subdirpaths = []

		# Make a subdirectories' paths list and filenames and paths list 
		for parentdirpath in dirpaths:
			subdirfilenames = os.listdir(parentdirpath)
			for name in subdirfilenames:
				path = os.path.join(parentdirpath, name)
				if os.path.isfile(path) :
					if self.notation_method == "relative" :
						if self.registered_extensions :
							if os.path.splitext(path)[1] in self.registered_extensions and path[0] == self.currentdir[0] : 
								self.filenamepathlist.append([name, path])
						else :
							if path[0] == self.currentdir[0] : 
								self.filenamepathlist.append([name, path])

					elif self.notation_method == "absolute" :
						if self.registered_extensions :
							if os.path.splitext(path)[1] in self.registered_extensions : 
								self.filenamepathlist.append([name, path])
						else :
							self.filenamepathlist.append([name, path])
				elif os.path.isdir(path):
					subdirpaths.append(path)

		# Recursive processing
		if len(subdirpaths) > 0 :
			self.make(subdirpaths)

		return self.filenamepathlist


