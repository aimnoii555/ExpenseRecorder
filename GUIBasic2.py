from tkinter import *
from tkinter import ttk, messagebox
import csv
from datetime import datetime
#ttk is theme of Tk

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Suksan')
GUI.geometry('600x700+500+50')

#--------------------------Menu----------------------------
menubar = Menu(GUI)
GUI.config(menu=menubar)

# File menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='import CSV')
filemenu.add_command(label='Export to Googlesheet')
#Help
def About():
    messagebox.showinfo('About','สวันดีครับ โปรแกรมนี้คือโปรแกรมบันทึกช้อมูล')

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
menubar.add_command(label='About',command=About)
#Donate
donatemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Donate',menu=donatemenu)



#-----------------------------------------------------------


Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
Tab.pack(fill=BOTH, expand=1)

icon_t1 = PhotoImage(file='wallet.png')
icon_t2 = PhotoImage(file='list.png')

Tab.add(T1, text=f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top') #.subsample(2) ย่อรูป
Tab.add(T2, text=f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2, compound='top')

F1 = Frame(T1)
#F1.place(x=150,y=50)
F1.pack()

days = {'Mon' : 'จันทร์',
        'Tue' : 'อังคาร',
        'Wed' : 'พุธ',
        'Thu' : 'พฤหัสบดี',
        'Fri' : 'ศุกร์',
        'Sat' : 'เสาร์',
        'Sun' : 'อาทิตย์'}

def Save(event=None):
    expense = v_expense.get()
    price = v_price.get()
    quantity = v_quantity.get()

    if expense == '':
        messagebox.showerror('Error','กรุณากรอกค่าใช้จ่าย')
        return
    elif price == '':
        messagebox.showerror('Error','กรุณากรอกราคา')
        return
    elif quantity == '':
        messagebox.showerror('Error','กรุณากรอกจำนวน')
        return

    try:
        total = int(price) * int(quantity)
        # .get() คือดึงค่ามาจาก v_expense = StringVar()
        print('รายการ: {} ราคา: {}'.format(expense, price))
        print('จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity, total))
        text = 'รายการ: {} ราคา: {}\n'.format(expense,price)
        text = text + 'จำนวน: {} รวมทั้งหมด: {} บาท'.format(quantity,total)
        v_result.set(text)

        # clear ข้อมูลเก่า
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')

        # บันทึกข้อมูล ลงใน csv อย่าลืม import csv ด้วย
        today = datetime.now().strftime('%a')  # days['Mon] = 'จันทร์'
        print(total)
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dt = days[today] + '-' + dt
        with open('savedata.csv', 'a', encoding='utf-8', newline='') as f:
            # with คือสั่งให้เปิดไฟล์ปิดอัตโนมัติ
            # 'a' การบันทึกเรื่อยๆ เพื่มข้อมูลต่อจากข้อมูลเก่า
            # newline='' ทำให้ข้อมูลไม่มีบรรท้ดว่าง
            fw = csv.writer(f)  # สร้างฟังชันสำหรับเชียนข้อมูล
            data = [dt, expense, price, quantity, total]
            fw.writerow(data)

            # ทำให้เคอเซอร์กลับไปต่ำแหน่งช่องกรอก E1
            E1.focus()
            update_table()


            messagebox.showinfo('success','successfully')
    except Exception as e:
        messagebox.showerror('Error','คุณกรอกข้อมูลไม่ถูกต้อง กรุณากรอกข้อมูลใหม่',e)
        v_expense.set('')
        v_price.set('')
        v_quantity.set('')
        #messagebox.showerror('error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
        #messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลข')


#ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = ('Angsana New',20) #None เปลี่ยนเป็น 'Angsana New'

#---------------------Image-----------------------

main_icon = PhotoImage(file='icon_list.png')
MainIcon = Label(F1,image=main_icon)
MainIcon.pack(pady=20)

#--------------------Text1----------------------------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1)
L.pack()
v_expense = StringVar()
# StringVar() คือตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#-------------------------------------------------

#--------------------Text2----------------------------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1)
L.pack()
v_price = StringVar()
#StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#-----------------------------------------------------

#-------------------------Text3---------------------------
L = ttk.Label(F1,text='จำนวน (ชิ้น)' ,font=FONT1)
L.pack()
v_quantity = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำรหับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()


#-----------------------------------------------------

icon_b1 = PhotoImage(file='save.png')

B2 = ttk.Button(F1,text=f'{"Save": >{10}}',image=icon_b1,compound='left',command=Save)
B2.pack(ipadx=50,ipady=20,pady=20)


v_result = StringVar()
v_result.set('------------ผลลัพธ์----------------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1,foreground='green')
result.pack(pady=5)
GUI.bind('<Tab>',lambda x: E2.focus())

#-------------------Tab 2------------------------

def read_csv():
    with open('savedata.csv',newline='',encoding='utf8') as f:
        fr = csv.reader(f)
        data = list(fr)
    return data

v_allrecord = StringVar()
Allrecord = ttk.Label(T2,textvariable=v_allrecord,font=(None,15),foreground='green')
Allrecord.pack()


header = ['วัน-เวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10)
resulttable.pack()

for hd in header:
    resulttable.heading(hd, text=hd)

headerwidth = [150,170,80,80,80]
for hd,w in zip(header,headerwidth):
    resulttable.column(hd,width=w)

def update_table():
    resulttable.delete(*resulttable.get_children())
    # for c in resulttable.get_children():
    #     resulttable.delete()
    data = read_csv()
    for dt in data:
        resulttable.insert('','end',value=dt)

update_table()
print('Get child:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()