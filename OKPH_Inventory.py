import sys
import random
import mysql.connector
# You need to import every new function you use btw
from PySide6 import *
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QApplication, QPushButton, QTableWidget, QTableWidgetItem, QMainWindow, QVBoxLayout, QPushButton, QWidget, QLabel, QHBoxLayout
from PySide6.QtGui import QPalette, QColor
##login information for mysql
testdb = mysql.connector.connect(
    host = "127.0.0.1",
    user = "testguy",
    password = "FiveFred3",
    database = "schema_b"
)
mycursor = testdb.cursor()

# establishes inventory table
cur_invn = [(0,"Walnuts",5.00)]

@Slot()
#clears and updates table with latest information
def refr_table():
    #Clears array and reads up to date info from sql table
    cur_invn.clear()
    shw = "SELECT * FROM donotinterfere_inv_placeholder"
    mycursor.execute(shw)
    myresult = mycursor.fetchall()
    for x in range(0,len(myresult)):
        cur_invn.append(myresult[x])
    print(cur_invn)
    #Distributes the information from cur_invn array into the table
    for i, (pk, item_desc, price) in enumerate(cur_invn):
        key = QTableWidgetItem(str(pk))
        item_name = QTableWidgetItem(str(item_desc))
        item_code = QTableWidgetItem(str(price))
        table.setItem(i, 0, key)
        table.setItem(i, 1, item_name)
        table.setItem(i, 2, item_code)
        table.setRowCount(len(cur_invn))
        table.setColumnCount(len(cur_invn[0]))

#testdb.commmit will only run once, so make sure to add it after any mysql changes
        #currently placeholder function that adds a entry to the mysql database with info from val and refreshes table
def say_b():
    sql = "INSERT INTO donotinterfere_inv_placeholder  VALUES (%s, %s, %s)"
    val = (0, "Pizza", 15.00)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchall()
    refr_table()
    print(cur_invn)

    testdb.commit()

#placeholder function that changes the price of all items of a certain type and refreshes
def say_w():
    sql = "UPDATE donotinterfere_inv_placeholder set price = '6.00' WHERE item_name = 'pizza'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    refr_table()
    print(cur_invn)

    testdb.commit()



app=QApplication(sys.argv)   

        #establishes table and row length
table = QTableWidget()
table.setRowCount(len(cur_invn))
table.setColumnCount(len(cur_invn[0]))
table.setHorizontalHeaderLabels(["key","Item_Desc", "Price"])

#Send Array to Table in MYSQL
#need to understand reading arrasy in python and for statement
for i, (pk, item_desc, price) in enumerate(cur_invn):
    sql = "INSERT INTO inv_placeholder VALUES (%s, %s, %s)"
    val = (0, cur_invn[i][0], cur_invn[i][1] )

#Code for button object (debug)
    
button1 = QPushButton("Bees")
# say_b function
button2 = QPushButton("Wasps")
# say_w function
button3 = QPushButton("Refresh")
# refr_table function

#ties button function to button press
button1.pressed.connect(say_b)
button2.pressed.connect(say_w)
button3.pressed.connect(refr_table)


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
        layout.addWidget(QLabel("budget: " + "$" + str("0.67")))
        layout.addWidget(table)
        layout.addWidget(button3)
        layout.addLayout(layout1)
        
#Dummy widget which layout is applied to
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

testdb.commit()

#Debug to check accuracy of python table
print(cur_invn)

#draws the table and executes app
main = inv_main()
main.show()
sys.exit(app.exec())