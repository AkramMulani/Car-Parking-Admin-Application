import threading
import tkinter.messagebox
from tkinter import *
import DBConnection as db
import machine
from Constraints import *


class App:
    def __init__(self):
        #########################################
        self.color=Color()
        self.font=Font()
        #########################################
        self.usernameAtLast=None
        self.locationAddressEntry = None
        self.locationAddressLabel = None
        self.locationAddButton = None
        self.locationNameEntry = None
        self.locationNameLabel = None
        self.addLocationButton = None
        self.addLocationLabel = None
        self.backButton = None
        self.locationsLabel = None
        self.root = Tk()
        self.mainFrame = Frame(self.root,width=1500,height=600,background=self.color.mainFrameColor)
        self.locationsList = Listbox(self.mainFrame, width=600, height=500, font=self.font.monospace,
                                     background=self.color.listBoxColor, foreground=self.color.white)
        self.usernameLabel = Label(self.mainFrame,text="Username / Email Id",font=self.font.impact,background=self.color.mainFrameColor)
        self.UserName = Entry(self.mainFrame, width=50,font=self.font.courier)
        self.passwordLabel = Label(self.mainFrame,text="Password :",font=self.font.impact,background=self.color.mainFrameColor)
        self.Password = Entry(self.mainFrame, width=50,font=self.font.courier, show='*')
        self.login = Button(self.mainFrame,width=15,text='>>>',font=self.font.serif,command=self.validate)

    def __start__(self):
        self.root.geometry("1000x600")
        self.root.title("Car Parking - (Admin)")
        self.root.minsize(1200,600)

        self.mainFrame.pack(side="left",anchor="s",fill=BOTH)
        self.usernameLabel.place(x=300,y=150)
        self.UserName.place(x=300,y=200)
        self.passwordLabel.place(x=300,y=300)
        self.Password.place(x=300,y=350)
        self.login.place(x=680,y=450)

        self.root.mainloop()

    def __close__(self):
        self.root.destroy()

    def loginFrame(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.root, width=1500, height=600, background=self.color.mainFrameColor)
        self.mainFrame.pack(side="left", anchor="s", fill=BOTH)
        self.locationsList = Listbox(self.mainFrame, width=600, height=500, font=self.font.monospace,
                                     background=self.color.listBoxColor, foreground=self.color.white)
        self.usernameLabel = Label(self.mainFrame, text="Username / Email Id", font=self.font.impact,
                                   background=self.color.mainFrameColor)
        self.UserName = Entry(self.mainFrame, width=50, font=self.font.courier)
        self.passwordLabel = Label(self.mainFrame, text="Password :", font=self.font.impact,
                                   background=self.color.mainFrameColor)
        self.Password = Entry(self.mainFrame, width=50, font=self.font.courier, show='*')
        self.login = Button(self.mainFrame, width=15, text='>>>', font=self.font.serif, command=self.validate)

        self.usernameLabel.place(x=300, y=150)
        self.UserName.place(x=300, y=200)
        self.passwordLabel.place(x=300, y=300)
        self.Password.place(x=300, y=350)
        self.login.place(x=680, y=450)

    def validate(self):
        if db.login(self.UserName.get(),self.Password.get()) == 1:
            self.usernameAtLast=str(self.UserName.get())
            tkinter.messagebox.showinfo("Success","Login Successfully... Thank You")
            self.afterSuccess()
        else:
            tkinter.messagebox.showwarning("Failure","Login Failed...Sorry!")

    def afterSuccess(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.root, width=1500, height=600, background=self.color.mainFrameColor)
        self.mainFrame.pack(side="left",anchor="s",fill=BOTH)
        self.backButton = Button(self.mainFrame,text="<-",width=5,font=self.font.courier,background=self.color.grey,foreground=self.color.backButtonColor,command=self.loginFrame)
        self.backButton.place(x=10,y=50)
        if db.getUsersLocation(self.usernameAtLast) is not None:
            self.userLocationLabel=Label(self.mainFrame,text='Your Location : {}'.format(db.getUsersLocation(self.usernameAtLast)),
                                         background=self.color.mainFrameColor,font=self.font.impact)
            self.userLocationLabel.place(x=10,y=100)
            self.userLocationAddressLabel=Label(self.mainFrame,text='Address : {}'.format(db.getUsersLocationAddress(db.getUsersLocation(self.usernameAtLast))),
                                                background=self.color.mainFrameColor,font=self.font.impact)
            self.userLocationAddressLabel.place(x=10,y=150)
            self.updateValuesBox=Frame(self.mainFrame,width=600,height=400,background=self.color.updateBoxColor,borderwidth=5,relief=RIDGE)
            self.updateValuesBox.place(x=200,y=200)
            self.TotalValue=Label(self.updateValuesBox,text='Total : {}',background=self.color.updateBoxColor,fg=self.color.white,
                                  font=self.font.timesNew)
            self.TotalValue.place(x=50,y=50)
            self.AvailableValue=Label(self.updateValuesBox,text='Available : {}',background=self.color.updateBoxColor,
                                      fg=self.color.white,font=self.font.timesNew)
            self.AvailableValue.place(x=50,y=100)
            if machine.isConnected():
                thread = threading.Thread(name='update values',target=self.updateValues())
                thread.start()
            else:
                tkinter.messagebox.showwarning("Warning",'Machine not connected yet...\nSo connect it first by USB')
        else:
            self.addLocationLabel = Label(self.mainFrame, text='Add New Location', font=self.font.impact,
                                          background=self.color.mainFrameColor)
            self.addLocationLabel.place(x=400, y=50)
            self.addLocationButton = Button(self.mainFrame, text='+', font=self.font.courier,
                                            command=self.addLocationNotExists)
            self.addLocationButton.place(x=700, y=50)
            self.locationsList = Listbox(self.mainFrame, width=600, height=500, font=self.font.monospace,
                                         background=self.color.listBoxColor, foreground=self.color.white)
            self.locationsList.place(x=10, y=150)
            l = db.getLocationsList()
            self.locationsList.configure(listvariable=StringVar(value=l))

    def addLocationNotExists(self):
        self.mainFrame.destroy()
        self.mainFrame = Frame(self.root,width=1500,height=600,background=self.color.mainFrameColor)
        self.mainFrame.pack(side=LEFT,anchor=S,fill=BOTH)
        self.backButton1 = Button(self.mainFrame,text='<<',font=self.font.courier,command=self.afterSuccess)
        self.backButton1.place(x=10,y=50)
        self.locationNameLabel = Label(self.mainFrame,text="Location Name",background=self.color.mainFrameColor,font=self.font.impact)
        self.locationNameLabel.place(x=100,y=100)
        self.locationNameEntry = Entry(self.mainFrame,width=50,font=self.font.monospace)
        self.locationNameEntry.place(x=100,y=170)
        self.locationAddressLabel = Label(self.mainFrame,text="Address",background=self.color.mainFrameColor,font=self.font.impact)
        self.locationAddressLabel.place(x=100,y=250)
        self.locationAddressEntry = Entry(self.mainFrame,width=50,font=self.font.monospace)
        self.locationAddressEntry.place(x=100,y=340)
        self.locationAddButton = Button(self.mainFrame,text="ADD Location",font=self.font.courier,background=self.color.grey,foreground=self.color.backButtonColor,command=self.addLocationName)
        self.locationAddButton.place(x=100,y=400)
        
        
    def addLocationName(self):
        name = str(self.locationNameEntry.get())
        address = str(self.locationAddressEntry.get())
        db.addLocation(self.usernameAtLast,name,address)

    def updateValues(self):
        while True:
                data = machine.read()
                if data is not None:
                    rec = data.split('-')
                    try:
                        total=rec[0]
                        space=rec[1]
                        self.TotalValue.configure(text='Total : {}'.format(total))
                        self.AvailableValue.configure(text='Available : {}'.format(space))
                        db.addData(db.getUsersLocation(self.usernameAtLast),total,space)
                    except:
                        print('data = {}'.format(data))
                else:
                    tkinter.messagebox.showerror("Error",'Can\'t read from machine...\nMake sure you are connected to your machine by USB')
