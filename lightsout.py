# -*- coding:utf-8 -*-

import numpy as np
import sys
import time
import os

class Lightsout:

    def __init__(self, L=5):
        self.L = L # lattice size
        p = 0.5
        lattice = np.random.random([self.L+2, self.L+2])
        self.lattice = lattice<p
        #i_latticeは全てFalseに揃える
        i_lattice = np.zeros([self.L+2, self.L+2])
        self.i_lattice = i_lattice>p
#        print "self.lattice: "
#        print self.lattice
        self.lattice[0,:] = self.lattice[self.L+1,:] = False
        self.lattice[:,0] = self.lattice[:,self.L+1] = False
        self.setmode = False
        self.solLine = 0

    def canvas_update(self):
        #clear display
        #os.system("cls")
        #os.system("clear")
        print ""
        l = ""
        for y in range(1,self.L+1):
            for x in range(1,self.L+1):
                if self.lattice[x,y]:
                    l += u" ■"
                else:
                    l += u" □"
            l += "\n"
        print l
        print ""

    def print_i(self):
        print "\n"
        l = ""
        for y in range(1,self.L+1):
            for x in range(1,self.L+1):
                if self.i_lattice[x,y]:
                    l += u" ■"
                else:
                    l += u" □"
            l += "\n"
        print l

    #各ライトのon/offを切り替える
    def changelight(self, m, n, i_mode=False):
        if i_mode:
            if self.i_lattice[m,n]:
                self.i_lattice[m,n] = False
            else:
                self.i_lattice[m,n] = True
        else:
            if self.lattice[m,n]:
                self.lattice[m,n] = False
            else:
                self.lattice[m,n] = True

    #ライトを押下する処理
    def pushlight(self, m, n, i_mode=False):
        self.changelight(m  ,n  ,i_mode) 
        if n-1>0:
            self.changelight(m  ,n-1,i_mode) 
        if m-1>0:
            self.changelight(m-1,n  ,i_mode) 
        if m+1<=self.L:
            self.changelight(m+1,n  ,i_mode) 
        if n+1<=self.L:
            self.changelight(m  ,n+1,i_mode) 

    #ライトを1つずつ切り替えるモードに移行
    def swichsetmode(self):
        if self.setmode:
            self.setmode = False
            print "swich normalmode"
        else:
            self.setmode = True
            print "swich setmode"

    def gatherligths(self, createfile=False, i_mode=False):
        if createfile:
            #print "[gather]createfile"
            #write ans_file
            f = open("ans.txt","a")
            buf = ""
            for num in range(1, self.L+1):
                buf += "0"
            buf += "\n"
            f.write(buf)
            for n in range(2,self.L+1):
                buf = ""
                for m in range(1,self.L+1):
                    if self.i_lattice[m,n-1]:
                    #if self.lattice[m,n-1]:
                        self.pushlight(m, n, True)
                        buf += "1"
                    else:
                        buf += "0"
                buf += "\n"
                f.write(buf)
            buf = ""
            for light in range(1, self.L+1):
                if self.i_lattice[light, self.L]:
                    buf += "1"
                else:
                    buf += "0"
            f.write(buf)
            f.write("\n\n")
            #refresh i_lattice
            i_lattice = np.zeros([self.L+2, self.L+2])
            self.i_lattice = i_lattice>0.2

            f.close()

        elif i_mode:
            #i_latticeにはgatherした時に押下するlightが示される
            #print "[gather]i_mode"
            for n in range(2,self.L+1):
                for m in range(1,self.L+1):
                    if self.i_lattice[m,n-1]:
                        self.pushlight(m, n, True)
                        self.changelight(m, n-1, True)
            buf = ""
            for m in range(1, self.L+1):
                if self.i_lattice[m, self.L]:
                    buf += "1"
                else:
                    buf += "0"
            for n in range(self.L,0,-1):
                for m in range(1,self.L+1):
                    if self.i_lattice[m,n-1]:
                        self.i_lattice[m,n]=True
                    else:
                        self.i_lattice[m,n]=False
            return buf

        else:
            #print "[gather]else"
            print u"\n □ □ □ □ □"
            for n in range(2,self.L+1):
                buf = ""
                for m in range(1,self.L+1):
                    if self.lattice[m,n-1]:
                        self.pushlight(m, n)
                        buf += u" ■"
                    else:
                        buf += u" □"
                print buf
            print ""
    
    #ansfileを作る
    def createansfile(self):
        print "[createfile]start"
        f = open("ans.txt","w")
        f.close
        #maxnum = self.L/2 + 1
        #for i in range(1, 2**maxnum):
        #上の条件ではself.L=6で網羅できなかった
        for i in range(1, 2**self.L):
            f = open("ans.txt","a")
            buf = ""
            for j in range(0, self.L):
                buf += str(i%2)
                i = i/2
            f.write(buf)
            f.write("\n")
            for m in range(0, self.L):
                if buf[m] == '1':
                    self.pushlight(m+1, 1, True)
            f.close()
            self.gatherligths(True)
        f.close()
        print "[createfile]done."


    #生成した問題の解があるかどうかを調べる
    def judgesolution(self):
        self.solLine = 0
        #refresh i_lattice
        i_lattice = np.zeros([self.L+2, self.L+2])
        self.i_lattice = i_lattice>0.2
        #print "[judgesolution]start"
        for m in range(1, self.L+1):
            for n in range(1, self.L+1):
                if self.lattice[m, n]:
                    self.i_lattice[m, n] = True
        buf = self.gatherligths(False, True)
        #print "[judgesolution]buf = ",
        #print buf
        #bufの型を下で読み込むitemListに合わせる
        buflist = []
        buflist.append(buf)

        f = open('ans.txt', 'r')
        itemList = []
        for line in f:
            #print "[judgesolurion]cp itemList = ",
            #print line
            itemList.append(line[:-1].split('\n'))
        f.close()

        if not "".join(itemList[self.L+3-1]) == "":
            self.createansfile()
            f = open('ans.txt', 'r')
            itemList = []
            for line in f:
                #print "[judgesolurion]cp itemList = ",
                #print line
                itemList.append(line[:-1].split('\n'))
            f.close()

        #print "[judgesolution]itemList = "
        #print itemList
        offset = self.L+3
        #use like offset+linefirst
        linefirst = 0
        howpush = 1
        solution = self.L+1
        for loffset in range(1, (2**self.L-1)*offset, offset):
            #print "[judgesolution]search itemList["+str(loffset+solution)+"]"
            #print itemList[loffset+solution-1]
            #itemListは[0]から始まる
            if itemList[loffset+solution-1] == buflist:
                print "[judgesolution]find!"
                self.solLine = loffset+solution
                print "[judgesolution]ansline = "+ "".join(itemList[self.solLine-self.L-2])
                return
        #print "[judgesolution]solution is nothing."
        return False

    #解を見つける処理
    def findsolution(self):
        print "[findsolution]start."
        self.judgesolution()
        if self.solLine == 0:
            print "[findsolution]error:can't find solution!!!!"

        f = open('ans.txt', 'r')
        itemList = []
        for line in f:
            #print "[findsolurion]cp itemList = ",
            #print line
            itemList.append(line[:-1].split('\n'))
        f.close()

        #refresh i_lattice
        i_lattice = np.zeros([self.L+2, self.L+2])
        self.i_lattice = i_lattice>0.2
        for m in range(1, self.L+1):
            for n in range(1, self.L+1):
                if self.lattice[m, n]:
                    self.i_lattice[m, n] = True
        buf = self.gatherligths(False, True)

        for n in range(2, self.L+1):
            ansLine = "".join(itemList[self.solLine-self.L-2+n])
            #print "[findsolution]ansLine = ",
            #print ansLine
            for m in range(1, self.L+1):
                #print "[findsolution]ansLine["+ str(m-1) +"]= ",
                #print ansLine[m-1]
                if ansLine[m-1] == "1":
                    self.changelight(m, n, True)

        ansLine = "".join(itemList[self.solLine-self.L-2])
        #print "[findsolution]last_ansLine = ",
        #print ansLine
        for m in range(1, self.L+1):
            if ansLine[m-1]=="1":
                #print "[findsolution]change i_lattice"
                self.changelight(m, 1, True)
        self.print_i()

    #コマンドの判定、実行
    def inputcommand(self):
        self.canvas_update()
        #標準入力を読む
        print "inputcommand\nnumber,number\nanswer\nset\nzero\n>",
        command = raw_input()
        #answerコマンドで解を探す関数を呼ぶ
        #reinit
        #set
        #gather
        #create
        #judge
        if command == "reset":
            self.__init__()
            self.judgesolution()
            while self.solLine == 0:
                self.__init__()
                self.judgesolution()
            print "[inputcommand]solLine = "+ str(self.solLine) 
            return 
        if command == "answer":
            self.findsolution()
            return 
        if command == "set":
            self.swichsetmode()
            return 
        if command == "gather":
            self.gatherligths()
            return 
        if command == "create":
            self.createansfile()
            return 
        if command == "judge":
            self.judgesolution()
            return 
        if command == "zero":
            lattice = np.zeros([self.L+2, self.L+2])
            self.lattice = lattice>0.2
            return 
        #カンマとコマンドの長さで構文エラーを判定、条件は改善の余地あり?
        if command.find(',')==-1 or command.find(',') != command.rfind(',') or len(command) > 30:
            print "sintax errer"
            print "Please input as number,number"
            print "continue to press enter key..."
            raw_input()
            return

        #コマンドを数値に変換
        buf = ""
        m = 0
        n = 0
        for letter in command:
            if letter == " ":
                continue
            elif letter == ",":
                if buf == "":
                    print "[inputcommand]sintax error"
                    break
                m = int(buf)
                buf = ""
                continue
            else:
                buf += letter
                #print "add " + letter + " to buff"
                continue
        n = int(buf)
        if m > self.L or n > self.L:
            print "errer: number too large"
            return
        if self.setmode:
            self.changelight(m, n)
        else:
            self.pushlight(m, n)

    def progress(self):
        #解判定用ファイルがなければ生成
        if not os.path.exists("./ans.txt"):
            self.createansfile()
        #解があるlatticeが生成出来るまで再生成
        self.judgesolution()
        while self.solLine == 0:
            self.__init__()
            self.judgesolution()
        print "[progress]solLine = "+ str(self.solLine) 

        try:
            while 1:
                lo.inputcommand()
        except KeyboardInterrupt:
            print "stopped."


if __name__ == '__main__':

    lo = Lightsout()
    lo.progress()
