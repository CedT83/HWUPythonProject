#!/usr/bin/python3
# -*- coding: iso-8859-1 -*-

################################## Imports
#We need to import tkinter to get GUI widgets
import tkinter as Tkinter


################################## Class
class View(Tkinter.Tk):
    #This is the constructor for this class
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        #We call the method that draws our GUI
        self.initialize()
        #The two lines below are just here to enhance the user experience by setting the cursor on the first input and allow him to use it easier
        self.entryDocument.focus_set()
        self.entryDocument.selection_range(0, Tkinter.END)

    def initialize(self):
        #We create a grid to organize the elements and define their position in the window
        self.grid()

################################## Entries
        
        #We have one entry to let the user enter the document UUID
        self.entryDocUuid = Tkinter.StringVar()
        self.entryDocument = Tkinter.Entry(self,textvariable=self.entryDocUuid)
        self.entryDocument.grid(column=0,row=1,sticky='EW')
        #Just a placeholder for the user
        self.entryDocUuid.set(u"Enter the Document UUID here")
        
        #We have one entry to let the user enter the reader UUID
        self.entryUserUuid = Tkinter.StringVar()
        self.entryUser = Tkinter.Entry(self,textvariable=self.entryUserUuid)
        self.entryUser.grid(column=0,row=3,sticky='EW')
        #Just a placeholder for the user
        self.entryUserUuid.set(u"Enter the User UUID here")

################################## Labels

        #Defines a label, to help the user 
        self.labelDocUuid = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelDocUuid,
                              anchor="w",fg="black")
        label.grid(column=0,row=0,columnspan=2,sticky='EW')
        #adds text to the label
        self.labelDocUuid.set(u"The document UUID:")
        
        #Another label
        self.labelUserUuid = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelUserUuid,
                              anchor="w",fg="black")
        label.grid(column=0,row=2,columnspan=2,sticky='EW')
        #adds text to the label
        self.labelUserUuid.set(u"The User UUID:")
        
        #Another label
        self.labelResult = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelResult,
                              anchor="w",fg="black")
        label.grid(column=0,row=4,columnspan=2,sticky='EW')
        #Adds text to the label
        self.labelResult.set(u"The result using the provided document is:")
        
################################## Buttons

        #This button will trigger the actions and 
        self.button = Tkinter.Button(self,text=u"Click me !",
                                command=None)
        self.button.grid(column=0,row=6)

        
################################## Other widgets

        #We create a Text widget that suits better our needs
        self.textResult = Tkinter.Text(self)
        #We want it to be read-only so we block its state
        self.textResult.config(state=Tkinter.DISABLED)
        #We place the widget on the window
        self.textResult.grid(column=0,row=5,columnspan=2,sticky='EW')

        #This is the listbox we use to let the user chose which action he wants to peform
        self.Lb1 = Tkinter.Listbox(self)
        #We add inputs with the corresponding (value, label) 
        self.Lb1.insert(0, "get countries")
        self.Lb1.insert(1, "get continents")
        self.Lb1.insert(2, "get browsers")
        self.Lb1.insert(3, "get readership")
        self.Lb1.insert(4, "get users that have read a document")
        self.Lb1.insert(5, "get documents read by a user")
        self.Lb1.insert(6, "get also-like")
        self.Lb1.insert(7, "get also-like by readership")
        self.Lb1.insert(8, "get also-like by popularity")
        
        #We place the widget on the window
        self.Lb1.grid(column=0,row=7)


################################## Rezising configurations
      
        #We create the configuration of the column 0
        self.grid_columnconfigure(0,weight=1)
        #We allow the windows to be resizable
        self.resizable(True,False)
        #We refresh the view with the geometry of the new window
        self.update()
        self.geometry(self.geometry())       



################################## setters & getters

    #Set method for the EntryUser widget
    def setEntryUser(self, text):
        self.entryUserUuid.set(text)
        
    #Get method for the EntryUser widget
    def getEntryUser(self):
        return self.entryUserUuid.get()
        
    #Set method for the EntryDocUuid widget
    def setEntryDocUuid(self, text):
        self.entryDocUuid.set(text)
        
    #Get method for the EntryDocUuid widget
    def getEntryDocUuid(self):
        return self.entryDocUuid.get()
      
    #Set method for the textbox widget  
    def setTextResult(self, data):
        #We want a read-only textbox so before writing we have to unlock the state of the widget
        self.textResult.config(state=Tkinter.NORMAL)
        #Then we can write
        #First we delete everything 
        self.textResult.delete(1.0, Tkinter.END)
        #Then we write
        self.textResult.insert(Tkinter.END, data)
        #Finally we block it again
        self.textResult.config(state=Tkinter.DISABLED)
        
    #Get method for the textbox widget
    def getTextResult(self):
        return self.textResult.get(0)
        
    #Set method for the listbox method
    def setSelectedListBox(self, value):
        self.Lb1.selection_set(value)
        
    #Get method for the listbox widget
    def getSelectedListbox(self):
        try:
            selected = self.Lb1.curselection()[0]
        except IndexError:
            selected = None
            tkMessageBox.showwarning("Oops", "You need to select an action")
        finally:
            return selected
        
    
    #To bind the controller and th view
    def register(self, controller):
        self.controller = controller
        
    #Just a wrapper for the mainloop method of Tkinter
    def main_loop(self):
        self.mainloop()
