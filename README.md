# pysideplus
```

this repo contain reusable beautifull pyside6 widgets.
you can use it instead  of pyside6 widgets because all original methods and attributes are available in this class
you can make subclass and use it as you  like.
for example TabPlusPlus (modified qtabwidget)  provides beautifull tab with  new tab button and tab history menu
```
### normal Qtabwidget
![image](https://github.com/user-attachments/assets/d3fe41fa-da66-47e2-8df0-c7a688623a81)
### extended widget
![image](https://github.com/user-attachments/assets/4d6a8c0e-5066-4c88-b6fa-007592d90899)

## usage
you can reuse this widget in your pyside code in two ways

#### * qt creator promote option
   
   this is the best choice. it is easy to create gui by drag and drop option in qt creator.
   when adding a tabwidget you can rightclick and select promote option to choose this extended class.
   so when it runs it will create instance of this class
   
#### * by subclassing / creating instance
   
```
 from customtabwidget import TabPlusPlus

 class modified_tab(TabPlusPlus):
    def _myTab__new_tab(self, event):
        print("new tab button clicked")

if __name__ == "__main__":
    print ( "test running" )
    from PySide6.QtWidgets import QApplication, QMainWindow
    import sys
    
    app = QApplication(sys.argv)
    widget = modified_tab()
    widget.setTabsClosable(True)
    widget.addTab(QPushButton("button 1"),"tab 0")
    widget.show()

    sys.exit(app.exec())
