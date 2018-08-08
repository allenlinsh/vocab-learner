# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 23:32:27 2018

@author: a2001
"""
import sys, os
import csv
import random
import subprocess
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QDesktopWidget, QPushButton, QLineEdit, QGridLayout, QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFileDialog, qApp
from PyQt5.QtCore import QTimer, QTime, Qt

if getattr(sys, 'frozen', False):
    # frozen
    scriptDir = os.path.dirname(sys.executable)
else:
    # unfrozen
    scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
f_path = scriptDir + os.path.sep
wl_path = f_path + 'word list\\'
filename = sys.argv[0].replace(f_path.replace('\\','/'), '')

path = wl_path + 'default.csv'
r_path = wl_path + 'review.csv'

#load and write .csv
def load_csv1():
    with open(f_path + 'test.csv', 'w', encoding='utf-8') as f2:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader) #skip the header
            wl1 = []
            test = ''
            for row in reader:
                vocab = ''
                vocab = row[0]
                
                df = ''
                df = row[1]
                
                tense = ''
                if row[2] == '1':
                    tense += '(n.)'
                if row[3] == '1':
                    tense += '(v.)'
                if row[4] == '1':
                    tense += '(adj.)'
                if row[5] == '1':
                    tense += '(adv.)'
                
                hint = ''
                hint = df + ' ' + tense
                
                wl1.append([vocab, hint])
                
            random.shuffle(wl1)
            for w in wl1:
                test += (w[0] + ',' + '"' + w[1] + '"' + '\n')
            f2.write(test)        
    
def load_csv2():
    with open(f_path + 'review_test.csv', 'w', encoding='utf-8') as f4:
        with open(r_path, 'r', encoding='utf-8') as f3:
            reader3 = csv.reader(f3)
            wl2 = []
            review = ''
            
            for row in reader3:
                vocab = ''
                vocab = row[0]
                
                hint = ''
                hint = row[1]
                
                wl2.append([vocab, hint])
                
            random.shuffle(wl2)
            for w in wl2:
                review += (w[0] + ',' + '"' + w[1] + '"' + '\n')
            f4.write(review)
    
"""

Main

"""
#load gui
class Main(QWidget):
    def __init__(self):
        super().__init__()
        
        #setup icon
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'icon.png'))
        
        self.initUI()
        
        #center/size & show        
        width = QDesktopWidget().width() * 0.3
        height = QDesktopWidget().height() * 0.3
        self.setMinimumSize(width, height)
        self.center()
        self.setWindowTitle('Vocab Trainer')            
        
    def initUI(self):        
        #textbox & font
        self.textbox0 = QLineEdit()

        self.font1 = self.textbox0.font()
        self.font1.setPointSize(14)
        
        self.textbox0.setFont(self.font1)
        
        #text
        label0 = QLabel('Select your word list:')
        label0.setFont(self.font1)
        
        label1 = QLabel('Created by Allen Lin. Latest Update: 2018.8.3')
        label1.setAlignment(Qt.AlignRight)
        
        #button1
        btn1 = QPushButton('Open')
        btn1.setFont(self.font1)
    
        self.btn2 = QPushButton('Learn')
        self.btn2.setFont(self.font1)
        
        self.btn3 = QPushButton('Review')
        self.btn3.setFont(self.font1)

        #setup grid
        grid0 = QGridLayout()
        grid0.setSpacing(20)
        grid0.addWidget(label0,0,0,1,0)
        grid0.addWidget(self.textbox0,1,0,1,1)
        grid0.addWidget(btn1,1,1,1,1)
        
        #button2 & 3
        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.btn3,0)
        vbox.addWidget(self.btn2,0)
        vbox.addWidget(label1,0)
        grid0.addLayout(vbox,2,0,2,0)
        
        self.setLayout(grid0)
        
        #select file
        def selectFile():
            self.textbox0.setText(''.join(QFileDialog.getOpenFileName()))   
            global path, r_path
            preload = self.textbox0.text()
            if preload != '':
                if preload[-4:] != '.csv':
                    a.textbox0.setText('')
                    a.popup = QMessageBox.about(a, 'Vocab Trainer', 'Please select .csv file.')
                else:
                    with open(preload, 'r', encoding='utf-8') as slt:
                        slt_r = csv.reader(slt)
                        header = next(slt_r)[0]
                        if header != 'Vocabulary':
                            path = self.textbox0.text()
                            r_path = wl_path + 'review.csv'
                        else:
                            r_path = self.textbox0.text()
                            path = wl_path + 'default.csv'
                        
        
        btn1.clicked.connect(selectFile)
    
    #center gui
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

"""

Trainer

"""
class Trainer(QWidget): 
    num = 0
    max_num = 0
    correct = 0
    dfn = ''
    res = ''
    ans = ''
    wl1 = [] 
    wl2 = []
    ms = '00:00:00'
    filename = ''
    revl = ''
    
    #processing
    def processing(self):
        #setup variables
        self.num = 0
        self.max_num = 0
        self.correct = 0  
        self.ms = '00:00:00'
        self.wl1 = [] 
        self.filename = ''
        self.revl = ''
        
        with open(f_path + 'test.csv', 'r', encoding='utf-8') as f2:
            reader2 = csv.reader(f2)
            for row in reader2:
                word = ''
                word = row[0]
                
                hint = ''
                hint = row[1]
                self.dfn = hint
                
                self.wl1.append([word, hint])
                self.max_num += 1
    
    #review
    def reviewing(self):
        #setup variables
        self.num = 0
        self.max_num = 0
        self.correct = 0
        self.ms = '00:00:00'
        self.wl2 = []
        self.filename = ''
        self.revl = ''
        
        with open(f_path + 'review_test.csv', 'r', encoding='utf-8') as f3:
            reader3 = csv.reader(f3)
            for row in reader3:
                word = ''
                word = row[0]
                
                hint = ''
                hint = row[1]
                self.dfn = hint
                
                self.wl2.append([word, hint])
                self.max_num += 1
    
    #next question
    def nextQ1(self, i):    
        if i < self.max_num:
            self.dfn = self.wl1[i][1]
            self.ans = self.wl1[i][0]
            self.label1.setText(str(self.dfn))
            self.label2.setText('')
            self.label_d.setText(str(self.num + 1) + '/' + str(self.max_num))
        else:
            #setup result
            self.max_n.setText(str(self.max_num))
            self.corr.setText(str(self.correct))
            self.percentage()
            self.min_sec.setText(str(self.ms))
            
            #print result
            self.rt = self.per.text()+'%'
            self.tm = self.min_sec.text()
            b.close()
            self.msgbox = QMessageBox.about(self, 'Results',
                                       'Accuracy: ' + self.rt + '\n' +
                                       'Time: ' + self.tm)
            self.time = QTime(0, 0, 0)
            #reboot
            b.close()
            subprocess.Popen([sys.executable, filename])
            
    #next question
    def nextQ2(self, i):    
        if i < self.max_num:
            self.dfn = self.wl2[i][1]
            self.ans = self.wl2[i][0]
            self.label1.setText(str(self.dfn))
            self.label2.setText('')
            self.label_d.setText(str(self.num + 1) + '/' + str(self.max_num))
        else:
            #setup result
            self.max_n.setText(str(self.max_num))
            self.corr.setText(str(self.correct))
            self.percentage()
            self.min_sec.setText(str(self.ms))
            
            #print result
            self.rt = self.per.text()+'%'
            self.tm = self.min_sec.text()
            b.close()
            self.msgbox = QMessageBox.about(self, 'Results',
                                       'Accuracy: ' + self.rt + '\n' +
                                       'Time: ' + self.tm)
            self.time = QTime(0, 0, 0)
            #reboot
            b.close()
            subprocess.Popen([sys.executable, filename])
            
        #calculate
    def percentage(self):
        c = self.correct
        t = self.max_num
        if (int(c) > 0 and int(t) > 0):
            p = float(c) / float(t) * 100
        else:
            p = 0.0
        self.per.setText(str(round(p,2)))
    
    #initiate
    def __init__(self):
        super().__init__()
        
        #setup icon
        self.setWindowIcon(QIcon(scriptDir + os.path.sep + 'icon.png'))
        
        self.initUI()
        
        #center/size & show        
        width = QDesktopWidget().width() * 0.4
        height = QDesktopWidget().height() * 0.4
        self.setMinimumSize(width, height)
        self.center()
        self.setWindowTitle('Vocab Trainer' + self.filename)   
    
    #initiate function
    def initUI(self):        
        #textbox & sizing font
        self.textbox1 = QLineEdit()
        self.font0 = self.textbox1.font()
        self.font0.setPointSize(18)
        self.textbox1.setFont(self.font0)
        
        #text
        self.label1 = QLabel(self.dfn)
        self.label1.setFont(self.font0)
        self.label1.setWordWrap(True);
        self.label1.setStyleSheet('background-color: #F5F5F5')
            
        self.label2 = QLabel('')
        self.label2.setFont(self.font0)
        self.label2.setStyleSheet('color: #FF0000')    
            
        #variable
        self.max_n = QLabel()
        self.corr = QLabel()
        self.per = QLabel()
        self.min_sec = QLabel()
        
        #button
        self.btn = QPushButton('Enter')
        self.btn.setFont(self.font0)
        
        self.textbox1.returnPressed.connect(self.btn.click)
        
        #timer & display
        self.label_t = QLabel(self.ms)
        self.label_t.setFont(Main().font1)
        self.label_d = QLabel()
        self.label_d.setFont(Main().font1)
        self.label_d.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
        self.timer = QTimer()
                
        self.time = QTime(0, 0, 0)
        self.timer.timeout.connect(self.timerEvent)
        self.timer.start(1000)    
        
        #timer & display
        hbox = QHBoxLayout()
        hbox.addWidget(self.label_t,0)
        hbox.addWidget(self.label_d,0)
        
        #setup grid
        grid1 = QGridLayout()
        grid1.setSpacing(50)
        grid1.addLayout(hbox,1,0,1,0)
        grid1.addWidget(self.label1)
        grid1.addWidget(self.label2)
        grid1.addWidget(self.textbox1)
        grid1.addWidget(self.btn)
        self.setLayout(grid1) 
        
    #setup timer
    def timerEvent(self):        
        if self.isVisible(): self.time = self.time.addSecs(1)
        self.ms = self.time.toString('hh:mm:ss')
        self.label_t.setText(self.ms)
        
    #center gui
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    
    #leave confirm
    def closeEvent(self, event):        
        if self.num < self.max_num:
            reply = QMessageBox.question(self, 'Vocab Trainer' + self.filename,
                "Are you sure to quit?", QMessageBox.Yes | 
                QMessageBox.No, QMessageBox.Yes)
        
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
                
    def keyPressEvent(self, event):
        #Close application from escape key.
        if event.key() == Qt.Key_Escape:
            #reboot
            b.close()
            subprocess.Popen([sys.executable, filename])
    
    #pressed enter
    def on_click1(self):        
        self.res = self.textbox1.text()
        
        if self.res != self.ans:
            self.textbox1.clear()
            self.label2.setText(self.ans)
        else:
            if self.label2.text() == '':
                self.correct += 1
            else:
                self.correct += 0
                with open(wl_path + 'review.csv', 'w', encoding='utf-8') as f3:
                    self.revl += (self.ans + ',' + self.dfn + '\n')
                    f3.write(self.revl)
            self.textbox1.clear()
            self.label2.setText('')
            self.num += 1
            self.nextQ1(self.num)
            
    #pressed enter
    def on_click2(self):        
        self.res = self.textbox1.text()
        
        if self.res != self.ans:
            self.textbox1.clear()
            self.label2.setText(self.ans)
        else:
            if self.label2.text() == '':
                self.correct += 1
            else:
                self.correct += 0
                with open(wl_path + 'review.csv', 'w', encoding='utf-8') as f3:
                    self.revl += (self.ans + ',' + self.dfn + '\n')
                    f3.write(self.revl)
            self.textbox1.clear()
            self.label2.setText('')
            self.num += 1
            self.nextQ2(self.num)

"""
Back-end
"""
    
def startTrainer():
    if a.textbox0.text() == '':
        a.warn = QMessageBox.about(a, 'Vocab Trainer', 'Please select a word list.')
    elif a.textbox0.text() == (wl_path + 'review.csv').replace('\\','/'):
        a.warn = QMessageBox.about(a, 'Vocab Trainer', 'Please select a word list.')
    elif b.max_num == 1:
        with open(path, 'w', encoding='utf-8') as f3:
            f3.write('')
        a.comp = QMessageBox.about(a, 'Vocab Trainer', 'The list is empty.')
    else:
        load_csv1()
        b.filename = ' - ' + (path[path.rfind('/')+1:])
        b.setWindowTitle('Vocab Trainer' + b.filename)
        b.processing()
        b.nextQ1(Trainer().num)
        b.btn.clicked.connect(b.on_click1)
        a.close()
        b.show()
        
def startReviewer():
    if a.textbox0.text() != (wl_path + 'review.csv').replace('\\','/') and a.textbox0.text() != '':
        a.warn = QMessageBox.about(a, 'Vocab Trainer', 'Please select a review list.')    
    elif b.max_num == 1:
        with open(wl_path + 'review.csv', 'w', encoding='utf-8') as f3:
            f3.write('')
        a.comp = QMessageBox.about(a, 'Vocab Trainer', 'The list is empty.')
        b.close()
        a.show()
    else:
        if b.max_num != 0 and a.textbox0.text() == '':
            a.comp = QMessageBox.about(a, 'Vocab Trainer', 'The list is empty.')
        else:
            load_csv2()
            b.filename = ' - review.csv'
            b.setWindowTitle('Vocab Trainer' + b.filename)
            b.reviewing()
            b.nextQ2(Trainer().num)
            b.btn.clicked.connect(b.on_click2)
            a.close()
            b.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Main()
    b = Trainer()
    a.show()
    
    if a.isVisible():
        a.btn2.clicked.connect(startTrainer)
        a.btn3.clicked.connect(startReviewer)
    
    sys.exit(app.exec_())