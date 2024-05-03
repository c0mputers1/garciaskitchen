import sys
import random
import mysql.connector

from PySide6 import *
from PySide6.QtCore import Slot, QSize
from PySide6.QtWidgets import QApplication, QPushButton, QTableWidget, QTableWidgetItem, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout, QTabWidget, QCheckBox, QComboBox, QLineEdit, QSizePolicy

##login information for mysql
testdb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "testguy",
    password = "TestPassword123",
    database = "schema_b"
)
mycursor = testdb.cursor()

#Home/Work dropdown box

# establishes inventory table where info will be stored
cur_invn = [(0,"Walnuts",5.00, 5, "grain")]

@Slot()

#clears and updates table with latest information
def refr_table(**kwargs):

    #Clears array and reads up to date info from sql table
    cur_invn.clear()
    src_param = kwargs.get('src_param', "")
    shw = "SELECT * FROM Gk_inventory" + src_param
    mycursor.execute(shw)
    myresult = mycursor.fetchall()
    for x in range(0,len(myresult)):
        cur_invn.append(myresult[x])
    print(cur_invn)
    #Distributes the information from cur_invn array into the table
    for i, (pk, item_desc, price, amount, type) in enumerate(cur_invn):
        key = QTableWidgetItem(str(pk))
        item_name = QTableWidgetItem(str(item_desc))
        item_code = QTableWidgetItem(str(price))
        item_amount = QTableWidgetItem(str(amount))
        item_type = QTableWidgetItem(str(type))
        table.setItem(i, 0, key)
        table.setItem(i, 1, item_name)
        table.setItem(i, 2, item_code)
        table.setItem(i, 3, item_amount)
        table.setItem(i, 4, item_type)
        table.setRowCount(len(cur_invn))
        table.setColumnCount(len(cur_invn[0]))

#Pulls all items from table and adds them to the drop down menu 
    item_box.clear()
    mycursor.execute("SELECT item_name FROM Gk_inventory")
    names = mycursor.fetchall()
    print(mycursor.fetchall())
    print(names)
    print("this is item box stuff")
    for y in range(len(names)):
        #filters out all unnecessary characters
        n = (str(names[y])).replace("(","")
        f = n.replace(")","")
        b = f.replace(",","")
        q = b.replace("'","")
        item_box.addItem(q)
        print(q)
        #print(names[y])

#Checks all categories, clers table, then adds them
#this table stores all unique categories
    Type_Box.clear()
    mycursor.execute("SELECT type FROM Gk_inventory;")
    types = mycursor.fetchall()
    types = list( dict.fromkeys(types))
    print(types)
    print("this is TYPE box stuff")
    for n in range(len(types)):
        n = (str(types[n])).replace("(","")
        f = n.replace(")","")
        b = f.replace(",","")
        q = b.replace("'","")
        print(q)
        #print(types[n])
        Type_Box.addItem(q)

    print(shw)
    #print(str(Attr_Box.currentText()))
    #print(str(Type_Box.currentText()))



#testdb.commmit will only run once, so make sure to add it after any mysql changes
        #Code that takes given values and searches for an item to add or subtract a given amount
def say_b(item_name, posneg, value):
    #Check for value initially
    mycursor.execute("SELECT * FROM Gk_inventory WHERE item_name = '" + item_name + "'")
    myresult = mycursor.fetchall()
    #Only runs if given item already is in the inventory
    if str(myresult) != "[]":
        print("This item exists!")
        mycursor.execute("SELECT amount FROM Gk_inventory WHERE item_name = '" + item_name + "'")
        res_amnt = mycursor.fetchall()
        #Converts current amount to string to remove from
        am1 = str(res_amnt[0]).replace(")","")
        am2 = am1.replace("(","")
        am3 = am2.replace(",","")
        print(res_amnt[0])
        print(am3)
        if (int(am3) - int(value)) >= 0:
            upd = "UPDATE Gk_inventory SET amount = amount " + str(posneg) + " '" + str(value) + "'" + " WHERE item_name = '" + item_name + "'"
            mycursor.execute(upd)
        else: 
            print("Negative Amount value!")
    refr_table()
    print(myresult)
    testdb.commit()

#Used to add new entries with new values to inventory
def say_w(item_desc, price, amount, type):
    add = "INSERT INTO Gk_inventory VALUES (%s, %s, %s, %s, %s)"
    val = (0, item_desc, float(price), int(amount), type)
    mycursor.execute(add, val)
    refr_table()
    print(cur_invn)
    testdb.commit()

def s_box_check():
    print("s_box_check works")
    if str(Attr_Box.currentText()) == "Type":
        Amnt_Box.setDisabled(True)
        Type_Box.setEnabled(True)
    elif str(Attr_Box.currentText()) == "Amount":
        Type_Box.setDisabled(True)
        Amnt_Box.setEnabled(True)

def search(attribute, type, amount):
    if Query.isChecked():
        if attribute == "Type":
            src = " WHERE " + str(attribute) + " = '" + str(type) + "'"
        elif attribute == "Amount":
            src = " WHERE Amount >= '" + amount + "'"
        refr_table(src_param = src)
        testdb.commit()
    else:
        refr_table()

#begins system
app=QApplication(sys.argv)  


#establishes table and row length
table = QTableWidget()
table.setRowCount(len(cur_invn))
table.setColumnCount(len(cur_invn[0]))
table.setHorizontalHeaderLabels(["Key","Item_Desc", "Price", "Amount", "Type"])
table.setSizePolicy(
        QSizePolicy.Policy.MinimumExpanding,
        QSizePolicy.Policy.MinimumExpanding
    )

#Code for button object (debug)
    
add_btn = QPushButton("Run")
# say_b function
item_box = QComboBox()
#determines whether a value will be added or subtracted
posneg_box = QComboBox()
#Amount to be added or subtracted from item vlaue
valu_box = QLineEdit()
#Displays all items from inventory
refr_btn = QPushButton("Refresh")
# refr_table function

valu_box.resize(QSize(1,30))

posneg_box.addItems(("-","+"))

#ties button function to button press
add_btn.pressed.connect(lambda : say_b(item_box.currentText(), posneg_box.currentText(), valu_box.displayText()))
refr_btn.pressed.connect(refr_table)

valu_box.setSizePolicy(
        QSizePolicy.Policy.Fixed,
        QSizePolicy.Policy.Fixed
    )


#!!Establishes query page!!
Query = QCheckBox("Search for Selected Categories?")

Attr_Box = QComboBox()
Type_Box = QComboBox()
Amnt_Box = QLineEdit()


Attr_Box.addItem("Type")
Attr_Box.addItem("Amount")

#Base for Widget page
QuWidget = QWidget()

Attr_Box.activated.connect(s_box_check)

Query.toggled.connect(lambda : search(Attr_Box.currentText(), Type_Box.currentText(), Amnt_Box.displayText()))



#Establishes base widget for item creation page
AddWidget = QWidget()
Add_Instruct0 = QLabel("Add new item name below")
Add_Instruct1 = QLabel("Add price per unit below")
Add_Instruct2 = QLabel("Add current amount below")
Add_Instruct3 = QLabel("Add item type below")
Add_Assistance = QLabel("See ReadMe for detailed instructions!")
Add_Submit = QPushButton("Add this item")
Add_Name = QLineEdit()
Add_Price = QLineEdit()
Add_Amnt = QLineEdit()
Add_Type = QLineEdit()


Add_Submit.pressed.connect(lambda : say_w(Add_Name.displayText(),Add_Price.displayText(), Add_Amnt.displayText(), Add_Type.displayText()) )


#establishes the main window
class inv_main(QMainWindow):
    def __init__(self):
        super(inv_main,self).__init__()

        self.setWindowTitle("Inviti") 
        self.setIcon("Inviti_icon.ico")

        #sets layout
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()

#Bottom row of buttons
        layout1.addWidget(add_btn)
        layout1.addWidget(posneg_box)
        layout1.addWidget(item_box)
        layout1.addWidget(valu_box)

#Layers all widgets from top to bottom
#        layout.addWidget(QLabel(str)))
        layout.addWidget(table)
        layout.addWidget(refr_btn)
        layout.addLayout(layout1)
        
#Widget for the main Page
        Mwidget = QWidget()
        Mwidget.setLayout(layout)

#Layout for Query page
        Q_Layout = QVBoxLayout()
        Q_Layout.addWidget(Query)
        Q_Layout.addWidget(Attr_Box)
        Q_Layout.addWidget(Type_Box)
        Q_Layout.addWidget(Amnt_Box)
        QuWidget.setLayout(Q_Layout)

#Layout for adding page
        A_Layout = QVBoxLayout()
        A_Layout.addWidget(Add_Instruct0)
        A_Layout.addWidget(Add_Name)
        A_Layout.addWidget(Add_Instruct1)        
        A_Layout.addWidget(Add_Price)
        A_Layout.addWidget(Add_Instruct2)        
        A_Layout.addWidget(Add_Amnt)
        A_Layout.addWidget(Add_Instruct3)        
        A_Layout.addWidget(Add_Type)
        A_Layout.addWidget(Add_Submit)
        A_Layout.addWidget(Add_Assistance)
        AddWidget.setLayout(A_Layout)



#Establishes tab widget, to which all other widgets are applied to
        Base = QTabWidget()

        Base.addTab(Mwidget, "&Main")
        Base.addTab(QuWidget, "&Search")
        Base.addTab(AddWidget, "&Add Items")
        Base.setCurrentWidget(Mwidget)

        self.setCentralWidget(Base)


#Ties search function to Query toggle



   

#Debug to check accuracy of python table
print(cur_invn)
print(valu_box.sizeHint)

#draws the table and executes app
refr_table()
main = inv_main()
main.show()
testdb.commit()

sys.exit(app.exec())