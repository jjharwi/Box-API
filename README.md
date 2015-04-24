Box-API
=======

Scripts and documentation for interacting with the Box API

To use the API, first check out https://developers.box.com and follow directions on how to create an application.  Once you've got an application created (hint: https://racker.app.box.com/developers/services/edit/), put "http://0.0.0.0/" in the redirect_uri field, and grab the client_id and client_secret to put them in .box_config.

Run Box_Setup.py to create the tokens section in .box_config and populate your initial access and refresh tokens.  It will present you with the proper URL to access your application, just open the URL and authenticate with your RSA token (use the Single Sign On link).  Then, click the "Grant access to Box" button. You will be presented with a URL in your browser that has "code=LONGSTRINGOFSTUFF" at the end.  Copy/paste the LONGSTRINGOFSTUFF into the script.  
 
The _refresh_token function will then be used by the other functions here and fetch you a new set of tokens whenever needed.  

At this point, if you have a particular folder you want to upload to, put it in the .box_config.  The [folders] section of the .box_config is where you need to put the folder_id for your root folder (0), or any other folder you own.  An example of how it should look is in box_config.ex

Once that is done, you can use these scripts to get information, upload, and update files in Box from the command line.

Box.py --

  _refresh_token updates your API and refresh tokens
  _file_upload creates a new file in your folder.
  _file_update updates an existing file in your folder.
  _file_download downloads a file from your folder to your local directory.
  _file_delete deletes a file in your Box folder.
  _file_info returns information about a file.
  _folder_info will give you info about your folder.  
  _folder_list will retrieve a list of files in the folder.

Box_Folderlist.py --
	Lists files in the Box folder.

Box_Fileinfo.py --
	Information about a file in Box

Box_Setup.py --
	Retrieves the initial access and refresh tokens after you authorize the application via RSA.
