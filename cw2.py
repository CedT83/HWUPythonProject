#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-
"""cw2.

Usage:
  cw2.py [-f <filename>] [-p | --pandas]
  cw2.py -u <user_uuid> -d <doc_uuid> -t <task_id> [-f | --file <filename>] [ --pandas ]
  cw2.py (-h | --help)
  cw2.py --version


Options:
  -h --help     Show this screen.
  -f --file     Specifies the file to read data from.
  --version     Show version.


"""

################################## Imports
#We need docopt to manage the comand line args for us
from libraries.docopt import docopt
import sys
#We need the three following imports to use our MVP pattern
import view as vw
import model as mdl
import presenter as pstr

################################## Main
if __name__ == '__main__':
    #We initialize docopt and give it the version number
    arguments = docopt.docopt(__doc__, version='cw2 1.6')
    
    #We define a variable to store the name of the file
    choosenFile = None
    #If the optional argument for the file is given
    if arguments['<filename>']:
        #we retrieve it
        choosenFile = arguments['<filename>']
    else:
        choosenFile = 'issuu.json'
    #we define a variable to know if pandas library is activated
    pandasLib = False
    #If pandas activated
    if arguments['--pandas']:
        #we set the variable to True
        pandasLib = True
    
    #Finally we instantiate our object Model using the defined or not filename
    try:
        with open(choosenFile) as _:
            pass
    except Exception:
        print("The specified file or default file: %s cannot be opened" % choosenFile)
        sys.exit(-1)
    model = mdl.Model(choosenFile, pandasLib)
    
    #If the script was launched using arguments we do not start the GUI and only use the Model object
    if arguments['<doc_uuid>'] and arguments['<user_uuid>'] and arguments['<task_id>']:
        model.extractData(arguments['<doc_uuid>'], arguments['<user_uuid>'], int(arguments['<task_id>']))
        model.draw()
    #Otherwise, no arguments given, we use the GUI
    else:
        #We create the two missing parts of the MVP to get the GUI
        app = vw.View(None)
        app.title('Coursework 2 - Data Analysis of a Document Tracker')
        cont = pstr.Presenter(model, app)
        #We call the infinite loop to display the GUI and use it
        app.mainloop()

