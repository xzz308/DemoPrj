from tkinter import *
import tkinter.messagebox

def clickCallback():
        tkinter.messagebox.askokcancel( "Hello Python", "Hello Runoob")

root = Tk()
root.geometry('250x340')
root.title('2048')
root.minsize(250,340)
root.maxsize(250,340)
root['background']='#FAF8EF'


frm_S = Frame(root,width=240,height=240,bg='#D4C8BD')
frm_NE1 = Frame(root,width=55,height=40,bg='#BBADA0')
frm_NE2 = Frame(root,width=55,height=40,bg='#BBADA0')

label_TITLE = Label(root,text='2048',width=4,font = 'Helvetica -44 bold',anchor='n',fg='#776E65',bg='#FAF8EF')
btn_RST = Button(root,text='New Game',width=10,bg='#8F7A66',fg='white',bd=0,font = 'Helvetica -12 bold',command=clickCallback)

label_SCORE = Label(frm_NE1,text='SCORE',bg='#BBADA0',fg='white',font = 'Helvetica -8')
label_BEST =Label(frm_NE2,text='BEST',bg='#BBADA0',fg='white',font = 'Helvetica -8')
label_nSCORE = Label(frm_NE1,text='0',bg='#BBADA0',fg='white',font = 'Helvetica -15 bold')
label_nBEST = Label(frm_NE2,text='0',bg='#BBADA0',fg='white',font = 'Helvetica -15 bold')

label_TITLE.grid(row=0,column=0,rowspan=2,sticky=NW,ipadx=3,ipady=15)
frm_NE1.grid(row=0,column=1,ipadx=10,pady=3)
frm_NE2.grid(row=0,column=2,ipadx=14,padx=5,pady=3)
btn_RST.grid(row=1,column=1,columnspan=2,padx=8,pady=5,sticky=SE)
frm_S.grid(row=2,column=0,columnspan=3,padx=6,pady=5,sticky=W)


label_SCORE.grid(row=0,column=0,sticky=W)
label_BEST.grid(row=0,column=0,sticky=W)
label_nSCORE.grid(row=1,column=0,sticky=W,ipadx=2)
label_nBEST.grid(row=1,column=0,sticky=W,ipadx=2)



root.mainloop()
