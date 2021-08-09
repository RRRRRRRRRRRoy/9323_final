# Meeting Archiving System

## Architecture

![avatar](C:\Users\user\Desktop\presentation\Technology.png)

## What's New

##### Previous version

1. Providing the login, signup and logout for the system.
2. providing the method for setting up the group.
3. providing the local recording for each group in the system.
4. providing the interface for each group to download the audio.

##### Current version

1. Fix the logic of the group
2. Adding the group search method for user
3. Adding the uploading files and downloading files for user
4. Adding transcription for mp4 files
5. Adding the online video play

## OS Platform Of Test and Development

Windows 10

## Demo Start

1. Download and install __PyCharm__
2. Import the Project into __PyCharm __
3. Install __MySQL server__;
4. Remember your ***port number*** and ***password***;
5. Create a scheme called ***meeting***;
6. Select the scheme built and run __meeting.sql__ to build the database;
7. Edit in __db.py__ around __row 8__:  
   * replace your username with __'root'__
   * replace your password with __'7788'__
   * replace your port with __3306__. (3306 is always the default port of MySQL server)
8. Run the script to install relative packages;

```shell script
	pip install -r requirements.txt
```

9. Register and Apply XFYUN API, click [here](https://www.xfyun.cn/services/lfasr). Then you can get ```APPID``` and ```SecreteKey``` (secrete key) for the permission of ***XFYUN*** Web API. Add these two in ```CONFIG.py```. ___XFYUN___ object.

10. Run the program via __app.py__ in PyCharm 

    ​	Or type the script in the terminal;

```shell script
	flask run
```

11. Finally, Open the html file, __index.html__ to start the system.

## Swagger Document

You can go to [__here__](https://editor.swagger.io/) to open this swagger document.

## Directory of Project

You can find the directory information of the project in this part.

```
├── .idea									// The configuration of VScode
├── __pycache__                 			// The Configuration of Pycharm
├── static                      			// The web pages of the projects
|	├── css                     			// The CSS layout for specific pages
|	│   ├── bootstrap.min.css		
│	│   ├── group.css              
│	│   ├── index.css         		
│	│   ├── login.css              
│	│   ├── online_session.css      
│	│   └── personal.css  
│	├── img									// Contain the image sources
│   ├── bootstrap-5.0.2-dist
|	├── js                      			// The CSS layout for specific pages
|	│   ├── API.js							// Utils based on jquery.min.js
|	│   └── jquery.min.js           		// the JQuery Framework
|	├── uploads								// Uploading and downloading folder	
│   ├── group.html				
│   ├── index.html				
│   ├── login.html				
│   ├── meeting.html			
│   ├── player.html  			
│   ├── upload.html 		
│   └── personal.html
├── utilities                      			// The web pages of the projects
|	├── transcription               		// The CSS layout for specific pages
|	│   ├── generate_transcription.py		// Transcription generator       
│   |	└── weblfasr_python3_demo.py 		// Basic API By XFyun
|	├── db.py								// DataBase configuration
|	└── CONFIG.py							// Normal configuration of project
├── Readme.md                   			// Help and Infomation
├── app.py                      			// The back-end entrance of the system
├── init.py									// Project Initializer
├── requirements.txt						// the package and version
└── Technology.png							// current Technology we used in this project

```

## XF Transcription

The current speech transcription of this project is provided by XFyun. This API is based on a deep full-sequence convolutional neural network, which can convert long segments of audio(smaller than 5 hours) data into text data. 

This kind of transcription is for recorded audio(not real-time). After files have been uploaded successfully, waiting for a few seconds, the server can return a JSON file which contains the best result of transcription. If the transfer time is longer than usual, there is a high probability that there will be a transfer peak in the current time period. Please wait patiently.

In addition, to make the transfer service smoother, please try your best to transfer audio files of more than 5 minutes. Uploading a large number of short audio may cause strain on the network and server resources, resulting in a backlog of tasks.

![avatar](./XFTranscription.png)

The efficiency of using XF transcription.

| Length of Audio(Minutes) | Time Of Getting Result(Minutes) |
| :----------------------: | :-----------------------------: |
|           X<10           |               Y<3               |
|         10<=X<30         |             3<=Y<6              |
|         30<=X<60         |             6<=Y<10             |
|          60<=X           |            10<=Y<20             |

