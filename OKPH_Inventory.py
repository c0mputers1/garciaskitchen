import sys
import random
import mysql.connector

from PySide6 import *
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QPushButton, QTableWidget, QTableWidgetItem, QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QTabWidget, QCheckBox, QComboBox, QTextEdit
##login information for mysql
testdb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "testguy",
    password = "FiveFred3",
    database = "schema_b"
)
mycursor = testdb.cursor()

# establishes inventory table
cur_invn = [(0,"Walnuts",5.00, 5, "grain")]
amnt_enbl = False
#establishes variable for inventory

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


#hey btw anyone from MIT, its me matthew r, just wanted to say I wrote like all of this program myself, as neither of my group memebers helped with any actual issues, that is why it is in such a sorry state
#testdb.commmit will only run once, so make sure to add it after any mysql changes
        #currently placeholder function that adds a entry to the mysql database with info from val and refreshes table
def say_b():
    add = "INSERT INTO donotinterfere_inv_placeholder  VALUES (%s, %s, %s, %s, %s)"
    val = (0, "Pepsi", 5.00, 3, "drink")
    mycursor.execute(add, val)
    myresult = mycursor.fetchall()
    refr_table()
    print(cur_invn)
    testdb.commit()

#placeholder function that changes the price of all items of a certain type and refreshes
def say_w():
    upd = "UPDATE donotinterfere_inv_placeholder set price = '6.00' WHERE item_name = 'pizza'"
    mycursor.execute(upd)
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
    
button1 = QPushButton("Add")
# say_b function
button2 = QPushButton("Test")
# say_w function
button3 = QPushButton("Refresh")
# refr_table function

#Establishes query page
Query = QCheckBox("Search for Selected Categories?")

Attr_Box = QComboBox()
Type_Box = QComboBox()
Amnt_Box = QTextEdit()


Attr_Box.addItem("Type")
Attr_Box.addItem("Amount")

#Base for Widget page
QuWidget = QWidget()

#ties button function to button press
button1.pressed.connect(say_b)
button2.pressed.connect(say_w)
button3.pressed.connect(refr_table)

h = 0

#establishes the main window
class inv_main(QMainWindow):
    def __init__(self):
        super(inv_main,self).__init__()

        #sets layout
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()

#Bottom row of buttons
        layout1.addWidget(button1)
        layout1.addWidget(button2)

#Layers all widgets from top to bottom
#        layout.addWidget(QLabel(str)))
        layout.addWidget(table)
        layout.addWidget(button3)
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


#Establishes tab widget, to which all other widgets are applied to
        Base = QTabWidget()

        Base.addTab(Mwidget, "&Main")
        Base.addTab(QuWidget, "&Search")
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