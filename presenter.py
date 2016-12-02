#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

################################## Imports
#We need no import here as we modify local variables and nothing else

################################## Class
class Presenter(object):
    #This is the constructor for this class
    #We need references of the view and the model in order to bind them using the controller
    def __init__(self, model, view):
        self.model = model
        self.view = view 
        #To add an event handler to an object in the view we will need the view to have the reference of the controller
        self.view.register(self)
        #Here we add the event handler
        self.view.button.bind("<Button>", self.performAction)
        
    #This is the main and only event handler we have, when we click on the button in the view, we manipulate the data in the model part 
    def performAction(self, event):
        #We have to make sure at least one action is selected
        if self.view.getSelectedListbox() == None:
            #If any is selected we quit the function
            return
        #We need to retrieve some data from the view before sending it to the model
        user = self.view.getEntryUser()
        task = self.view.getSelectedListbox()
        doc = self.view.getEntryDocUuid()
        #We ask the model for data
        self.model.extractData(doc, user, task)
        #Then we update the view
        self.view.setTextResult(self.model.getData())
        #We create the histogram to display the results
        ########################################################### TOMODIFY
        print("please modify before submission")
        self.model.draw()
