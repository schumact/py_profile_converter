# Py Profile Converter

The contents of this repo will automate the transferring of profiles between
your favorite sneaker bots. Constantly entering the same information into different
bots over and over again can be time consuming and annoying. With this python program, 
you just need to supply an existing file containing your profiles from one of the supported
bots and a new profile file will be created for another one of the supported bots. 

##Prerequisites 

Have python 3 downloaded. This script was tested on version 3.7.2. There
are no third party modules in use so older python 3 versions should suffice.

## Installing

Simply download the file from github to a directory of your choosing.

## Running the Program

Running the program is simple as well. All that's needed is to run main.py and pass 
the required arguments arguments -t, -f, -n and the path of your existing profile file. For 
a description of each option, run main.py with the -h or --help flag. 

-t: the bot in which a new profile file is to be created

-f: the bot whose profile file is being used to create the new file

-n: name of new profile file with appropriate file extension. (Every profile file extension
is .json besides anb which is .csv) 

```python main.py -f <bot_name> -t <bot_name> -n <new_file> <existing_profile_file>```

#### Find a bug or want a new bot added
Feel free to email me at schumact@protonmail.com if you want a new bot to be added to the script
or if you have any questions. If a bot isn't supported, then that's probably because I'm not in 
possession of it and I don't know how that bot formats its profiles. I'd be happy to add other bots
if someone would email me a profile file with test profile(s) in it. 