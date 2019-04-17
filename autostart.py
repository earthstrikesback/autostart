import sys
import os
from pathlib import Path


import pyforms
from pyforms.basewidget import BaseWidget
from pyforms.controls import ControlText
from pyforms.controls import ControlButton
from pyforms.controls import ControlFile
from pyforms.controls import ControlLabel
from pyforms.controls import ControlCheckBoxList





class AutoStartPrograms(BaseWidget):
    def __init__(self):
        super(AutoStartPrograms,self).__init__('Autostart programs')

        self._selectScript = ControlFile('select startup script: ')
        self._selectScript.changed_event = self.SelectScriptChanged

       
        self._autoStartList = ControlCheckBoxList('autostart items')
        self._autoStartList.value = self.AutoStartList()
        self._autoStartList.changed_event = self.AutoStartListChanged
   
   # delete button
        self._buttonDelete = ControlButton('delete')
        self._buttonDelete.value = self._buttonDeleteAction
   
   # close button
        self._buttonClose = ControlButton('close')
        self._buttonClose.value = self._buttonCloseAction



    def AutoStartScriptSet(self):
        script = self._selectScript.value
        if script != '':
            self._label.value = script
            self.writeAutoStartScript(script)
            self.alert("script set as autostart" + script)

    def writeAutoStartScript(self,script):
        scriptContent = self.AutoStartFileContent(script)
        f = open(self.AutoStartFullName(), "w")
        f.write(scriptContent)
        f.close()
    
    # close button
    def _buttonCloseAction(self):
        sys.exit()

    # delete button
    def _buttonDeleteAction(self):
        index = self._autoStartList.selected_row_index
        deleteFile = self.AutoStartFolder() + self.AutoStartListIndex(index)
        os.remove(deleteFile)
        self.AutoStartListRefresh()


    # functions
    def AutoStartFolder(self):
        return(str(Path.home()) + '/.config/autostart/')

    def AutoStartFileName(self):
        scriptfile = self._selectScript.value
        return(os.path.basename(scriptfile) + '.desktop')

    def AutoStartFullName(self):
        return(self.AutoStartFolder() + self.AutoStartFileName())

    def AutoStartFileContent(self,scriptFile):
        text =  "[Desktop Entry]\n"
        text = text + "Exec=" + scriptFile
        text = text + """


Name=screen
Terminal=false
Type=Application
StartupNotify=false
"""
        return(text)

    def AutoStartList(self):
        allentries = [] 
        for entry in os.listdir(self.AutoStartFolder()):
            if os.path.isfile(os.path.join(self.AutoStartFolder(), entry)):
                if(entry.endswith('.desktop')):
                    allentries += [(entry,True)]
                else:
                    allentries += [(entry,False)]
        return(allentries)
    


    def AutoStartListRefresh(self):
        self._autoStartList.clear()
        self._autoStartList.value = self.AutoStartList()

    def AutoStartFilesList(self):
        allentries = [] 
        for entry in os.listdir(self.AutoStartFolder()):
            if os.path.isfile(os.path.join(self.AutoStartFolder(), entry)):
               allentries += [entry]
        return(allentries)
   
    def AutoStartListIndex(self,index):
        filesList = self.AutoStartFilesList()
        return(filesList[index])

    def SelectScriptChanged(self):
        self.AutoStartScriptSet()
        self.AutoStartListRefresh()


    def AutoStartListChanged(self):
        checkedindexes = self._autoStartList.checked_indexes
        itemsCount = self._autoStartList.count
        files = self.AutoStartFilesList()
        for i in range(itemsCount):
            checked = False
            for t in checkedindexes:
                if t == i :
                    checked = True
            self.setAutoStart(self.AutoStartFolder() + str(files[i]),checked)

    def setAutoStart(self,autostartfile,status):
        if(autostartfile.endswith('.desktop') and status == False):
            os.rename(autostartfile,autostartfile[:-8])
        if(autostartfile.endswith('.desktop')==False and status == True):
            os.rename(autostartfile,autostartfile + '.desktop')





if __name__ == "__main__" : pyforms.start_app( AutoStartPrograms, 
            geometry = (1900,400,400,400) 
        )


