from urllib import request
from tkinter import *
import tkinter.messagebox as messagebox
from ftplib import FTP
import os,re
def pictureselect(glassID):
    d=r'http://10.30.50.103/fsweb/fs/fs01_s2_get.jsp?pid=/b1data/%s/%s/%s/%s/img/%s_gls_boe_1.jpg'%(glassID[:5],glassID[5:11],glassID[11:13],glassID[13:15],glassID[5:])
    request.urlretrieve(d,r'C:\Users\124804\Desktop\glass_map\%s.jpg'%glassID[5:])

class Application(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.glassIDs=Label(self,text='请输入带有工序号的GLASS ID：')
        self.glassIDs.pack()
        self.glassIDs_Entry=Entry(self)
        self.glassIDs_Entry.pack()
        self.download=Button(self,text='下载GLASS图片',command=self.function1)
        self.download.pack()
        self.panelIDs=Label(self,text='请输入带有工序号的PANEL ID：')
        self.panelIDs.pack()
        self.panelIDs_Entry=Entry(self)
        self.panelIDs_Entry.pack()
        self.download_panel=Button(self,text='下载PANEL图片',command=self.function2)
        self.download_panel.pack()        
        
    def function1(self):
        glassIDs=self.glassIDs_Entry.get()
        tardir=r'C:\Users\124804\Desktop\glass_map'
        if not os.path.isdir(tardir):
            os.mkdir(tardir)  
        IDlist=glassIDs.split(';')
        IDlist_nospace=[]
        for x in IDlist:
            if x:
                IDlist_nospace.append(x.lower())
        for glassID in IDlist_nospace:
            try:
                pictureselect(glassID)
            except:
                pass

#    def download_img(self,panelID):
#        ftp.cwd('/b1data/%s/%s/%s/%s/img/'%(panelID[0:5],panelID[5:11],panelID[11:13],panelID[13:15]))
#        list_img = ftp.nlst()
#        str_img = ';'.join(list_img)
#        pattern = re.compile(r'%s.*?\.jpg'%panelID[5:])
#        list_target= re.findall(pattern,str_img)
#        for img in list_target:
#            try:
#                with open(r'C:\Users\124804\Desktop\panel_img\%s'%img,'wb') as f:
#                    ftp.retrbinary('RETR %s'%img,f.write)
#            except:
                #print('%s 下载失败'%img)
#                pass
    
    def function2(self):
        panelIDs=self.panelIDs_Entry.get()
        target_dir = r'C:\Users\124804\Desktop\panel_img'
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        ftp = FTP('10.30.50.103')
        ftp.login('mmifs','boefs123')
        IDlist = panelIDs.split(';')
        for panelID in IDlist:
            if not panelID:
                continue
            try:
                ftp.cwd('/b1data/%s/%s/%s/%s/img/'%(panelID[0:5],panelID[5:11],panelID[11:13],panelID[13:15]))
                list_img = ftp.nlst()
                str_img = ';'.join(list_img)
                pattern = re.compile(r'%s.*?\.jpg'%panelID[5:])
                list_target= re.findall(pattern,str_img)
                for img in list_target:
                    try:
                        with open(r'C:\Users\124804\Desktop\panel_img\%s'%img,'wb') as f:
                            ftp.retrbinary('RETR %s'%img,f.write)
                    except:
                        pass
            except:
                pass
        ftp.quit()

app=Application()
app.master.title('不良图下载')
app.master.geometry('500x300+500+200')
app.mainloop()
#if __name__=='__main__':
#    glassIDs=input('请输入带有工序号的GLASS ID：')
#    tardir=r'C:\Users\124804\Desktop\glass_map'
#    if not os.path.isdir(tardir):
#        os.mkdir(tardir)  
#    start=time.clock()
#    print('download is starting...')
#    IDlist=glassIDs.split(';')
#    IDlist_nospace=[]
#    for x in IDlist:
#        if x:
#            IDlist_nospace.append(x.lower())
#    for glassID in IDlist_nospace:
#        try:
#            print('%s is starting...'%glassID)
 #           pictureselect(glassID)
 #           print('%s is end...'%glassID)
 #       except:
 #           print('%s map图下载失败'%glassID)
#    print('download ending')
#    end=time.clock()
#    print('程序用时：%d'%(end-start))
#    time.sleep(10)


