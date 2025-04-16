# pysideplus
```

this repo contain reusable beautifull pyside6 widgets.you can use it instead  of pyside6 widgets
for example TabPlusPlus (modified qtabwidget).it is inherited from Qtabwidget
   it provides beautifull tab with  new tab button and tab history menu and tab search bar
```
### pyside6 normal Qtabwidget
![image](https://github.com/user-attachments/assets/d3fe41fa-da66-47e2-8df0-c7a688623a81)
### pysideplus  TabPlusPlus widget (modified Qtabwidget)
![image](https://github.com/user-attachments/assets/e0e72c1f-f5c9-4352-8675-cc9b793f720a)

## usage
you can reuse these custom widgets in your pyside code in two ways

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
```


## Webview usage

> Webview provides http connection monitering ability. that is not available in original webview of pyside6.
> 
> originalwebview can only read request headers not body but this webview can aacess full request and responce

```
   from pysideplus import webview2.webview as webview
   import sys
   from PySide6.QtWidgets import QApplication
   from PySide6.QtCore import QUrl

   class mywebview ( webview.Webview ):
        def on_http_connection (self, flow ) :
            print ( "connection received " )

   if __name__ == "__main__":
       app = QApplication(sys.argv)
       window = mywebview()
       window.setUrl(QUrl("https://www.python.org"))
       window.show()
       sys.exit(app.exec())
```
