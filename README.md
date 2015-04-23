Box-API
=======

Scripts and documentation for interacting with the Box API

To use the API, first check out https://developers.box.com and follow directions on how to create an application.  Once you've got an application created (hint: https://racker.app.box.com/developers/services/edit/), you can put the client_id and client_secret in the box-token.py script and generate access and refresh tokens.  The Box_Refresh function will then be used by the other functions here and fetch you a new set of tokens whenever needed.

To initially populate your .box_config file, run the box-token.py script with your application credentials.  The [folders] section of the .box_config is where you can put the folder_id for your root folder (0), or any other folder you own.

Once that is done, you can use these scripts to get information, upload, and update files in Box from the command line.  I'm still working on the download and delete operations.

Box_Folder.py --
	Primary folder functions.  _folder_info will give you info about your root folder.  _folder_list will retrieve a list of files in the folder you designated in .box_config

Box_Folderlist.py --
	Lists files in the Box folder.

Box_Fileinfo.py --
	Information about a file in Box

Box_File.py --
	Primary file functions.  _file_upload creates a new file.  _file_update updates an existing file with a new version.  _file_info pulls file attributes.

Box_Refresh.py --
	Retrieves access and refresh tokens for use by OAuth2.

box-token.py --
	Retrieves the initial access and refresh tokens after you authorize the application via RSA.


