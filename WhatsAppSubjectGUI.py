import codecs, sys, datetime
from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import showerror

global filename, timeOrdered, lifetimeOrdered, subjectTimes
filename = ""
timeOrdered = []
lifetimeOrdered = []
subjectTimes = []

class SubjectFrame(Frame):
    global filename
    def __init__(self):
        Frame.__init__(self)
        self.pack()
        self.master.title("WhatsApp Subject Viewer")
        self.master.rowconfigure(7,weight=1)
        self.master.columnconfigure(1,weight=1)
        
        self.selectbutton = Button(self, text="Select exported WhatsApp chat file", command=self.LoadFile,width=51,height=2)
        self.selectbutton.grid(row=0, column=0, columnspan=2, sticky=N)
        
        self.filelabel = Label(self, fg="red", text="No file selected", width=50, height=2, anchor=CENTER)
        self.filelabel.grid(row=1, column=0, columnspan=2, sticky=N)
        
        self.processbutton = Button(self, fg="green", text="Analyse", state=DISABLED, command=self.Process,width=51,height=2)
        self.processbutton.grid(row=2, column=0, columnspan=2, sticky=N)


        self.spacer = Label(self, text="", height=1)
        self.spacer.grid(row=3, column=0, columnspan=2, stick=N)
        
        self.printlifetime = Button(self, text="Print ordered\nby lifetime",state=DISABLED, command=PrintLifetime, width=25,height=2)
        self.printlifetime.grid(row=4, column=0, stick=N)
        
        self.exportlifetime = Button(self, text="Export ordered\nby lifetime", state=DISABLED, command=ExportLifetime, width=25,height=2)
        self.exportlifetime.grid(row=4, column=1, stick=N)

        self.printtime = Button(self, text="Print ordered\nby time",state=DISABLED, command=PrintTime, width=25,height=2)
        self.printtime.grid(row=5, column=0, stick=N)
        
        self.exporttime = Button(self, text="Export ordered\nby time", state=DISABLED, command=ExportTime, width=25,height=2)
        self.exporttime.grid(row=5, column=1, stick=N)
        
        self.grid(sticky=W+E+N+S)
        
    def LoadFile(self):
        global filename, timeOrdered
        filename = askopenfilename(defaultextension=".txt",filetypes=[('WhatsApp Chat Export File', ".txt"),('All Files', ".*")],title="Load WhatsApp Export File")
        
        if filename[-4:]==".txt":
            print("Accepted file type")
            self.filelabel["text"]=filename
            self.filelabel["fg"]="green"
            self.processbutton["state"]=NORMAL
            
        elif filename=="":
            print("No file selected")
            self.filelabel["text"]="No file selected"
            self.filelabel["fg"]="red"
            self.processbutton["state"]=DISABLED
            self.DisableExports()
            
        else:
            print("Invalid file type")
            self.filelabel["text"]="Invalid file type"
            self.filelabel["fg"]="red"
            self.processbutton["state"]=DISABLED
            self.DisableExports()

    def EnableExports(self):
        global timeOrdered
        self.printlifetime["state"]=NORMAL
        self.exportlifetime["state"]=NORMAL
        self.printtime["state"]=NORMAL
        self.exporttime["state"]=NORMAL
        self.spacer["text"] = str(len(timeOrdered))+" subject changes"

    def DisableExports(self):
        self.printlifetime["state"]=DISABLED
        self.exportlifetime["state"]=DISABLED
        self.printtime["state"]=DISABLED
        self.exporttime["state"]=DISABLED
        self.spacer["text"] = ""
        
    def Process(self):
        global filename
        #try:
        if True:
            testFile = codecs.open(filename,"r",encoding="utf-8").readlines()
            CheckSubjects()
            self.EnableExports()
            
        #except:
        #    showerror("Error","File based error, possibly wrong encoding?")
        #    self.DisableExports()

def PrintLifetime():
    global lifetimeOrdered
    for i in range(0,len(lifetimeOrdered)):
        print(str(lifetimeOrdered[i][1]),lifetimeOrdered[i][0])
    print()
    
def ExportLifetime():
    global lifetimeOrdered
    toSave = asksaveasfilename(title="Save export file",filetypes=[('Text file', ".txt")])
    try:
        writeStr = ""
        if toSave==filename:
            showerror("Error","Can't overwrite the WhatsApp export file.")
            return
        
        print("Writing to file "+toSave)
        for i in range(0,len(lifetimeOrdered)):
            writeStr+=str(lifetimeOrdered[i][1])+"mins "+lifetimeOrdered[i][0]
            writeStr+="\n"
        with codecs.open(toSave,"w",encoding="utf-8") as f:
            f.write(writeStr.translate(dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)))
        print("Exported to file.")
    except FileNotFoundError:
        showerror("Error","No file given to save to")
    
def PrintTime():
    global timeOrdered, subjectTimes
    for i in range(0,len(timeOrdered)):
        print(datetime.datetime.strftime(subjectTimes[i],"%d/%m/%Y %H:%M"),timeOrdered[i])
    print()
    
def ExportTime():
    global timeOrdered, subjectTimes
    toSave = asksaveasfilename(title="Save export file",filetypes=[('Text file', ".txt")])
    try:
        writeStr = ""
        if toSave==filename:
            showerror("Error","Can't overwrite the WhatsApp export file.")
            return
        print("Writing to file "+toSave)
        for i in range(0,len(timeOrdered)):
            writeStr+=datetime.datetime.strftime(subjectTimes[i],"%d/%m/%Y %H:%M")+" "+timeOrdered[i]
            writeStr+="\n"
        with codecs.open(toSave,"w") as f:
            f.write(writeStr.translate(dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)))
        print("Exported to file.")
    except FileNotFoundError:
        pass

def CheckSubjects():
    global filename, lifetimeOrdered, timeOrdered, subjectTimes
    file = codecs.open(filename,"r", encoding="utf-8").readlines()
    print("Processing",len(file),"lines...")
    translationTable = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

    subjectChanges = []
    isWhatsApp=False
    oldStyle=False
    
    for line in file:
        if "changed the subject from" in line:
            subjectChanges.append(line)
            isWhatsApp=True
            if "“" in line:
                oldStyle=True

    if isWhatsApp==False:
        showerror("Error","File does not have any subject changes, if its a WhatsApp export at all.")
        return
    
    justSubjects = []
    subjectTimes = []
    for item in subjectChanges:
        item = item.translate(translationTable)
        if oldStyle==True:    
            justSubjects.append(item.split("“")[2].split("”")[0])
        else:
            justSubjects.append(item.split('"')[3].split('"')[0])
        
        time = item[:18].replace(",","").replace(" ","").replace("/","").replace(":","")
        structTime = datetime.datetime.strptime(time,"%d%m%Y%H%M")
        subjectTimes.append(structTime)
        
    subDict = {}
    for i in range(0,len(justSubjects)):
        if i==len(justSubjects)-1:
            time = file[-1][:18].replace(",","").replace(" ","").replace("/","").replace(":","")
            lastMsgTime = datetime.datetime.strptime(time,"%d%m%Y%H%M")
            lifetime = abs((lastMsgTime-subjectTimes[i]))
        else:
            lifetime = abs((subjectTimes[i+1]-subjectTimes[i]))
        subDict[justSubjects[i]] = lifetime

    timeOrdered = justSubjects
    lifetimeOrdered = sorted(subDict.items(), key=lambda kv: kv[1], reverse=True)
    print("Processed. Ready for print and export.\n")

if __name__=="__main__":
    SubjectFrame().mainloop()
