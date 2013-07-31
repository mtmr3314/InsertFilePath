================
 InsertFilePath
================

This plug-in is for Sublime Text 2 only!  
This plug-in's function is so simple!  
It is inserting a certain file path at the cursor! Just one!  
And by using quick panel, searching the file name and path is so easy!  
In addition, you can select that the inserted path is absolute or relative!  



How to Use
==========

Pressing `ctrl+i` and `a` or `r` continuously,  will activate quick panel.  
Next, selecting file name on the quick panel, the `absolute` or `relative` file path is inserted at the cursor.

These searchable files with quick panel are all files contained in the current folder, project folders, 
`repository` folders that you can set or combination of these.
Furthermore you can set searchable file extensions and whether including these folders as search target.  



Settings
========

```JSON
"include_current_dir": bool,
"include_project_dirs": bool,
"include_open_files": bool,
"include_repository_dirs": bool,

"repository": ["path1", "path2", ... ],
"target_extensions": [".ext1", ".ext2", ... ]
```


`include_...` settings are whether including files contained these folders and OPEN FILES as search target.
By default, all settings are only `true`.  
`repsitory` setting is registering the paths as the above `repository` folders by setting folders' full-path in the list.  
`target_extensions` setting is defined searchable file extensions. As an example, if setting is above, 
files with `.ext1`, `.ext2` and other `...` extensions are only displayed on the quick panel. 
By default, there are not settings.   



Getting Started
===============

Download zip from github url or add repository and install using Package Control.

	https://github.com/mtmr3314/InsertFilePath.git



Attention
=========

Checked on windows 7 only.

英語はGoogle翻訳通してまともな日本語に変換されるレベルでいいかな程度にしか考えてません(´ｰ`)y-~~




==================

28.Jul.2013 : ver.1.1  Probably work on Sublime Text 3  
27.Jul.2013 : ver.1.0  Release
