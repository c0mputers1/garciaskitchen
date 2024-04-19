import sys
import random
import mysql.connector

from PySide6 import *
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QPushButton, QTableWidget, QTableWidgetItem, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout, QTabWidget, QCheckBox, QComboBox, QTextEdit
##login information for mysql
testdb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "testguy",
    password = "TestPassword123",
    database = "schema_b"
)
mycursor = testdb.cursor()

# establishes inventory table where info will be stored
cur_invn = [(0,"Walnuts",5.00, 5, "grain")]

@Slot()

#clears and updates table with latest information
def refr_table(**kwargs):

    #Clears array and reads up to date info from sql table
    cur_invn.clear()
    src_param = kwargs.get('src_param', "")
    shw = "SELECT * FROM donotinterfere_inv_placeholder" + src_param
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

    print(shw)
    print(str(Attr_Box.currentText()))
    print(str(Type_Box.currentText()))



#testdb.commmit will only run once, so make sure to add it after any mysql changes
        #currently placeholder function that adds a entry to the mysql database with info from val and refreshes table
def say_b(item_name):
    #Check for value initially
    mycursor.execute("SELECT * FROM donotinterfere_inv_placeholder WHERE item_name = '" + item_name + "'")
    myresult = mycursor.fetchall()
    #Only runs if given item already is in the inventory
    if str(myresult) != "[]":
        print("This item exists!")
        mycursor.execute("SELECT amount FROM donotinterfere_inv_placeholder WHERE item_name = '" + item_name + "'")
        res_amnt = mycursor.fetchall()
        print(res_amnt)
        upd = "UPDATE donotinterfere_inv_placeholder SET amount = amount + '1' WHERE item_name = '" + item_name + "'"
        mycursor.execute(upd)
    refr_table()
    print(myresult)
    testdb.commit()

#Used to add new entries with new values to inventory
def say_w(item_desc, price, amount, type):
    add = "INSERT INTO donotinterfere_inv_placeholder VALUES (%s, %s, %s, %s, %s)"
    val = (0, item_desc, float(price), int(amount), type)
    mycursor.execute(add, val)
    refr_table()
    print(cur_invn)
    testdb.commit()

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

#gets each row and adds info to mysql
#check why there is no code to execute this later
for i, (pk, item_desc, price, amount, type) in enumerate(cur_invn):
    sql = "INSERT INTO inv_placeholder VALUES (%s, %s, %s, %s, %s)"
    val = (0, cur_invn[i][1], cur_invn[i][2], cur_invn[i][3], cur_invn[i][4] )

#Code for button object (debug)
    
add_btn = QPushButton("Add")
# say_b function
item_box = QComboBox()
#Displays all items from inventory
refr_btn = QPushButton("Refresh")
# refr_table function

item_box.addItems(("Pizza","Pepsi","Burger","Coke"))

#Establishes query page
Query = QCheckBox("Search for Selected Categories?")

Attr_Box = QComboBox()
Type_Box = QComboBox()
Amnt_Box = QTextEdit()


Attr_Box.addItem("Type")
Attr_Box.addItem("Amount")

#Base for Widget page
QuWidget = QWidget()

Query.toggled.connect(lambda : search(Attr_Box.currentText(), Type_Box.currentText(), Amnt_Box.toPlainText()))

#ties button function to button press
add_btn.pressed.connect(lambda : say_b(item_box.currentText()))
refr_btn.pressed.connect(refr_table)

#Establishes base widget for item creation page
AddWidget = QWidget()
Add_Instruct = QLabel("Inlcude the information formatted as (0, name of the item, price of the item, amount of the item, category of item)")
Add_Assistance = QLabel("See ReadMe for detailed instructions!")
Add_Submit = QPushButton("Add this item")
Add_Name = QTextEdit()
Add_Price = QTextEdit()
Add_Amnt = QTextEdit()
Add_Type = QTextEdit()


Add_Submit.pressed.connect(lambda : say_w(Add_Name.toPlainText(),Add_Price.toPlainText(), Add_Amnt.toPlainText(), Add_Type.toPlainText()) )

#establishes the main window
class inv_main(QMainWindow):
    def __init__(self):
        super(inv_main,self).__init__()

        #sets layout
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()

#Bottom row of buttons
        layout1.addWidget(add_btn)
        layout1.addWidget(item_box)

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
        A_Layout.addWidget(Add_Instruct)
        A_Layout.addWidget(Add_Name)
        A_Layout.addWidget(Add_Price)
        A_Layout.addWidget(Add_Amnt)
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



    if str(Attr_Box.currentText()) == "Type":
        Type_Box.clear()
        Type_Box.addItem("food")
        Type_Box.addItem("drink")


#Ties search function to Query toggle
    Query.toggled.connect(lambda : search(Attr_Box.currentText(), Type_Box.currentText(), Amnt_Box.toPlainText()))


#Debug to check accuracy of python table
print(cur_invn)

#draws the table and executes app
main = inv_main()
main.show()
testdb.commit()

sys.exit(app.exec())