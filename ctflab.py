
 
__author__ = "dawood abbaspour"
__license__ = "ctfos"
 
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtCore, QtGui
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QCompleter
import webbrowser
import os, os.path, zipfile
from PyQt5.QtCore import QStringListModel, Qt
import syntax
import fldb 
import subprocess
from tkinter import filedialog
from tkinter import *
import platform
class SmartCompleter(QCompleter):
    model = QStringListModel()
    strings = ["one", "two", "THREE"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.model.setStringList(self.strings)
        self.setModel(self.model)
    def insert(self,str1):
       
       if str1!="":
        self.strings.append(str1)
        self.model.setStringList(self.strings)
        self.setModel(self.model)
    def clear(self):
        self.strings = []
        self.model.setStringList(self.strings)
        self.setModel(self.model)
    def getlen(self):
        return len(self.strings)
class LineNumberArea(QWidget):
 
    line=""
    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor
 
 
    def sizeHint(self):
        return Qsize(self.editor.lineNumberAreaWidth(), 0)
 
 
    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)
        if self.line!="":
          s=self.line,self.toPlainText()
          self.line=""
 
class CodeEditor(QPlainTextEdit):
    line=""
    filetext=""
    filezip="";
    zipfiles=""
    global oldpath
    sc=SmartCompleter()
    dbfile=""
    def __init__(self, parent = None):
        super(CodeEditor,self).__init__(parent)
         
        self.highlight = syntax.PythonHighlighter(self.document())
        
        self.lineNumberArea = LineNumberArea(self)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.setFont(font)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        #print(self.updateLineNumberAreaWidth)
        self.updateLineNumberAreaWidth(0)
        self.completer = self.sc
        self.completer.setWidget(self)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseSensitive)
        self.completer.activated.connect(self.insert_completion)

    def insert_completion(self, completion):
        global allkey
      
        if completion == self.completer.completionPrefix():
            return
        text_cursor = self.textCursor()
    
        last_chars = len(completion) - len(self.completer.completionPrefix())
        user=fldb.Key("","","",self.dbfile)
        try:
            a=user.find_key_content(completion[-last_chars:])
            for s in a:
             if s!="":
              text_cursor.insertText(s)
        except:
         pass
        self.setTextCursor(text_cursor)   
    def text_before_cursor(self):
        text_cursor = self.textCursor()
        text_cursor.select(QtGui.QTextCursor.WordUnderCursor)
        return text_cursor.selectedText()
    def lineNumberAreaWidth(self):
        digits =1
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        count = max(1, self.blockCount())
        count2=self.blockCount()
        #print("ssf",count2)
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
         
          
        return space
        
 
    def updateLineNumberAreaWidth(self, _):
        global pre
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)
        
    def updateLineNumberArea(self, rect, dy):
        
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                       rect.height()/2)
 
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)
 

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        cr = self.contentsRect();
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                    self.lineNumberAreaWidth(), cr.height()))
    def text_before_cursor(self):
        text_cursor = self.textCursor()
        text_cursor.select(QtGui.QTextCursor.WordUnderCursor)
        return text_cursor.selectedText()
    def runonzip(self,cmd,zipfile2):
        if zipfile2!="":
         dir2=zipfile2.replace(".zip","")
         dir1= os.path.dirname(os.path.realpath(zipfile2))
         y = zipfile.ZipFile(zipfile2,'a')
         y.extractall(dir2) 
         os.chdir(dir2)
         self.dbfile=dir1+"\\"+os.path.basename(zipfile2).replace(".zip","")+"\\"+os.path.basename(zipfile2).replace(".zip",".db")
         self.dbfile=self.dbfile.replace('\\', '/')
         print("dbfile",self.dbfile)
         print("cmd1",cmd)
         if os.system(cmd)==0:
          os.chdir(dir1)
          y.close()
        else:
            print("cmd",cmd)
            os.system(cmd)
    def openzip(self,zipfile2):
        if zipfile2!="":
         dir2=zipfile2.replace(".zip","")
         dir1= os.path.dirname(os.path.realpath(zipfile2))
         y = zipfile.ZipFile(zipfile2,'a')
         y.extractall(dir2) 
         os.chdir(dir2)
         if platform.system()=='Windows':
          self.dbfile=dir1+"\\"+os.path.basename(zipfile2).replace(".zip","")+"\\"+os.path.basename(zipfile2).replace(".zip",".db")
          textfile=dir1+"\\"+os.path.basename(zipfile2).replace(".zip","")+"\\"+os.path.basename(zipfile2).replace(".zip",".txt")
         if platform.system()=='Linux':
          self.dbfile=dir1+"/"+os.path.basename(zipfile2).replace(".zip","")+"/"+os.path.basename(zipfile2).replace(".zip",".db")
          textfile=dir1+"/"+os.path.basename(zipfile2).replace(".zip","")+"/"+os.path.basename(zipfile2).replace(".zip",".txt")
         with open(textfile) as f:
          self.setPlainText(self.toPlainText()+"\n"+ f.read())
         self.dbfile=self.dbfile.replace('\\', '/')
         print("dbfile",self.dbfile)
          
    def openfile(self):
        global oldpath
        global dbfile
        files = QtWidgets.QFileDialog.getOpenFileName(None,'OpenFile',"/home/dawood/Desktop/ctf/lfedito")
        if ".zip" in files[0]:
         self.zipfiles=files[0]
         self.openzip(self.zipfiles)
        elif ".db" in files[0]:
          self.dbfile=files[0]
          print("opened db",self.dbfile)
        elif ".tm" in files[0]:
          self.zipfiles=files[0]
          os.move(files[0],files[0].replace(".tm",".zip"))
          print("zip",files[0].replace(".tm",".zip"))
          self.openzip(self.zipfiles)
        else:
         with open(files[0]) as f:
          self.setPlainText(self.toPlainText()+"\n"+ f.read())
         f.close()
        self.setPlainText(self.toPlainText.replace("#openfile",""))
    def savefile(self):
        files = QtWidgets.QFileDialog.getOpenFileName(None,'SaveTextFile','/')
        with open(files[0],'w') as f:
            f.write(self.toPlainText().replace("#filesave",""))
            f.close()
    def zipconsole(self,str):
         str=str.replace(">","")
         zip = zipfile.ZipFile(str)
         self.setPlainText(self.toPlainText()+"\n"+str+">"+ (zip.namelist()))
          
    def FileDialog(self,directory='', forOpen=True, fmt='', isFolder=False):
     options = QFileDialog.Options()
     options |= QFileDialog.DontUseNativeDialog
     options |= QFileDialog.DontUseCustomDirectoryIcons
     dialog = QFileDialog()
     dialog.setOptions(options)

     dialog.setFilter(dialog.filter() | QtCore.QDir.Hidden)

    # ARE WE TALKING ABOUT FILES OR FOLDERS
     if isFolder:
        dialog.setFileMode(QFileDialog.DirectoryOnly)
     else:
        dialog.setFileMode(QFileDialog.AnyFile)
    # OPENING OR SAVING
     dialog.setAcceptMode(QFileDialog.AcceptOpen) if forOpen else dialog.setAcceptMode(QFileDialog.AcceptSave)

    # SET FORMAT, IF SPECIFIED
     if fmt != '' and isFolder is False:
        dialog.setDefaultSuffix(fmt)
        dialog.setNameFilters([f'{fmt} (*.{fmt})'])

    # SET THE STARTING DIRECTORY
     if directory != '':
        dialog.setDirectory(str(directory))
     else:
        dialog.setDirectory(str(ROOT_DIR))


     if dialog.exec_() == QDialog.Accepted:
        path = dialog.selectedFiles()[0]  # returns a list
        return path
     else:
        return ''
    def executeline(self,line,str):
     if "#new" in str:
         self.setPlainText("")
     if "#openfile" in str:
        self.openfile()
     if "#filesave" in str:
        
        self.savefile()
     if "pyrun" in str:
         
        self.filetext=self.toPlainText().replace("#pyrun","").replace(">>>","")
        lines=self.filetext.splitlines()
        self.filetext="";
        for s in lines:
         if not "#run" in s:
          self.filetext+=s+"\n";
          if "#run" in s:
            self.filetext="" 
        with open("temp.py","w+") as f:
             f.write(self.filetext);
             f.close()
        if "pyrun2" in str:
            os.system("python2 temp.py")
        else:
            print("cmd3")
            os.system("python temp.py")
        os.remove("temp.py")
        #self.setPlainText(self.toPlainText().replace("#pyrun",""));
     
     elif "cpprun" in str:
        self.filetext=self.toPlainText().replace("#cpprun","")
        lines=self.filetext.splitlines()
        self.filetext="";
        for s in lines:
         if not "#run" in s:
          self.filetext+=s+"\n";
         if "#run" in s :
            self.filetext=""       
        with open("temp.cpp","w") as f:
             f.write(self.filetext);
             f.close()
        os.system("g++ -o temp.o temp.cpp")
        if os.path.isfile("temp.o"):
             print("compiled succesfully")
             os.system("./temp.o")
        os.remove("temp.cpp") 
     
        #self.setPlainText(self.toPlainText().replace("#cpprun",""));
     elif "crun" in str:
         self.filetext=self.toPlainText().replace("#crun","")
         lines=self.filetext.splitlines()
         self.filetext="";
         for s in lines:
          if not "#run" in s:
           self.filetext+=s+"\n";
         if "#run" in s:
            self.filetext=""       
         with open("temp.c","w") as f:
             f.write(self.filetext);
             f.close()
         os.system("g++ -o temp.o temp.c")
         if os.path.isfile("temp.o"):
             print("compiled succesfully")
             os.system("./temp.o")
         os.remove("temp.c") 
         #self.setPlainText(self.toPlainText().replace("#crun",""));
     elif  "#delete" in self.line:
           content=""
           self.line=self.line.replace("#delete","")
           words=self.line.split(".")
           fldb.delete_key(words[0])
     elif  "#save" in str:
           content=""
           self.line=str.replace("#save","")
           words=self.line.split(".")
           lists=self.toPlainText().splitlines()
           for line1 in lists:
               if not "#save" in line1:
                   content+=line1+"\n";
                   
                   print("saving..")
           user = fldb.Key(words[0],content,words[1], "googlectf2020.db")
     else:
         str=str.replace("$","")
         str=str.replace("#run","")
         if "cddir" in str:
          str=str.replace("cddir","")
          files = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
          os.chdir(files)
         elif ".zip" in str:
             self.zipconsole(str)
         else:
          if not "#save" in str:
           os.system(str.replace("#run",""))
              
    def lineNumberAreaPaintEvent(self, event):
        
        mypainter = QPainter(self.lineNumberArea)
 
        mypainter.fillRect(event.rect(), Qt.black)
 
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()
 
        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber )
                co=int(number)+1
                lists=self.toPlainText().splitlines()
                
                #if len(lists)>0:
                # print("df",lists[co])
                try:
                    
                 #if len(lists)>int(number):
                 # print(lists[int(number)])
                  if lists[int(number)]!="":
                   self.line=lists[int(number)]
                 
                except:
                  pass
                mypainter.setPen(Qt.white)
                mypainter.drawText(0, top, self.lineNumberArea.width(), height,
                 Qt.AlignRight, number)
 
            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1
 
 
    def highlightCurrentLine(self):
        global allkeys
        global dbfile
        extraSelections = []
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        number = str(blockNumber )
       
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.black)
 
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
            lines=self.toPlainText().splitlines()
            y = self.textCursor().blockNumber() + 1;
            x = self.textCursor().columnNumber() + 1;
            self.completer = self.sc
            text_before_cursor = self.text_before_cursor()
            self.sc.clear()
            self.completer.popup().isVisible()
            self.sc.clear()
            users=fldb.Key("","","", self.dbfile)
            try:
             a=users.get_all__key(lines[y-1])
             for s in a:
                if s!="":
                 self.sc.insert(s)
            except:
                pass
            if self.completer.getlen()==0:
               self.completer.popup().hide()
            else:
             self.completer.popup().show()
            text_before_cursor = self.text_before_cursor()
            if text_before_cursor !=     self.completer.currentCompletion():
               if text_before_cursor !=self.completer.completionPrefix():
                
                #self.completer.setCompletionPrefix(lines[y-1])
                #self.completer.setCompletionPrefix(":")
                self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

                cursor_rectangle = self.cursorRect()
                popup = self.completer.popup()
                if lines[y-1]=="":
                    self.completer.popup().hide()
                cursor_rectangle.setWidth(popup.sizeHintForColumn(0) + popup.verticalScrollBar().sizeHint().width())
                self.completer.complete(cursor_rectangle)
                if self.completer.getlen()==0:
                    self.completer.popup().hide()
            else:
              #self.completer.popup().hide()
              pass
            '''try:
             self.sc.clear()
             users=fldb.Key("","","", "fldb.db")
             a=users.get_all__key(lines[y-1])
             for s in a:
               self.sc.insert(s)
            except:
                 pass'''
            
      

            
            s=self.toPlainText();
            try:
            
             if lines[y-1].endswith("#save"):
               #lines[y-1]=lines[y-1].replace("#save","")
               self.executeline(s,lines[y-1])
             elif lines[y-1].endswith("#cpprun"):
              lines[y-1]==lines[y-1].replace("#cpprun","")
              lines=s.splitlines()
              self.executeline(s,"#cpprun")
             elif lines[y-1].endswith("#crun"):
              lines[y-1]=lines[y-1].replace("#crun","")
             
              self.executeline(s,"#crun")
             elif lines[y-1].endswith("#pyrun"):
              lines[y-1]=lines[y-1].replace("#pyrun","")
              lines=s.splitlines()
              self.executeline(s,"#pyrun")
             elif lines[y-1].endswith("#pyrun2"):
              lines[y-1]=lines[y-1].replace("#pyrun","")
              lines=s.splitlines()
              self.executeline(s,"#pyrun2")
             elif lines[y-1].endswith("#new"):
              #s=lines[y-1].replace("#pyrun","")
              lines=s.splitlines()
              self.executeline(s,"#new")
             elif lines[y-1].endswith("#openfile"):
              #s=lines[y-1].replace("#pyrun","")
              lines=s.splitlines()
              self.executeline(s,"#openfile")
             elif lines[y-1].endswith("#exit"):
                print("exit")
                QCoreApplication.quit()
             elif lines[y-1].endswith("#openweb"):
                    lines[y-1]=lines[y-1].replace("#openweb","")
                    webbrowser.open(lines[y-1])
             elif lines[y-1].endswith("#filesave"):
              #s=lines[y-1].replace("#pyrun","")
              lines=s.splitlines()
              self.executeline(s,"#filesave")
             else:
              if(lines[y-1].endswith("#run")):
               self.setPlainText(self.toPlainText().splitlines()[y-1].replace("#run",""))
               lines[y-1]=lines[y-1].replace("#run","")
               s=lines[y-1].replace("#run","")
               s=s.replace("$","")
               if "cddir" in s:
                   s=s.replace("cddir","")
                   files = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
                   os.chdir(files)
               elif "openweb" in s:
                   
                    s=s.replace("openweb","")
                    webbrowser.open(s) 
               elif (lines[y-1].endswith("zip>")):
                   self.zipconsole(s);
               else:
                 self.runonzip(s,self.zipfiles)
            except:
             pass
            #try:
             #print(lines[y-1],":",x-1)
            #except:
             #pass
        self.setExtraSelections(extraSelections)
 
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    pre=""
    dbfile=""
    oldpath="/"
    app = QApplication(['ctflab'])
    app.setApplicationName("ctflab")
    print(sys.argv)
    codeEditor = CodeEditor()
    codeEditor.resize(900, 600)
    codeEditor.setStyleSheet("background-color:black;color:white;background-repeat: no-repeat; background-position: center;")
    allkeys=[]
    #with open("syntax.py","r") as f:
       # codeEditor.setPlainText(f.read())
    codeEditor.show()    
    sys.exit(app.exec_())
