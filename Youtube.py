from tkinter import *
from pytube import YouTube

#Tk() used to initialize tkinter to create display window
#geometry() used to set the window’s width and height
#resizable(0,0) set the fix size of window
#title() used to give the title of window

root = Tk()
root.geometry('500x500')
root.resizable(0,0)
root.title("Rao Youtube Downloder")

Label(root,text = 'Youtube Video Downloader', font ='arial 20 bold').pack()

link = StringVar()

Label(root, text = 'Paste Link Here:', font = 'arial 15 bold').place(x= 160 , y = 60)
link_enter = Entry(root, width = 70,textvariable = link).place(x = 32, y = 90)

def Downloader():
    url =YouTube(str(link.get()))
    video = url.streams.first()
    video.download()
    Label(root, text = 'DOWNLOADED', font = 'arial 15').place(x= 180 , y = 210)

Button(root,text = 'DOWNLOAD', font = 'arial 15 bold' ,bg = 'pale violet red', padx = 2, command = Downloader).place(x=180 ,y = 150)

root.mainloop()