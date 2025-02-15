
from PySide6.QtWidgets import ( QTabWidget, QWidget, QPushButton,QHBoxLayout, QLineEdit)
from PySide6.QtCore import Qt,QObject, QEvent
from PySide6.QtGui import QFont,QAction,QIcon

import styleconfig
from qmenu import CustomQmenu
from scrollable_qmenu import ScrollableMenu
from pathlib import Path
import re

__author__ = "github.com/its-me-abi"
__version__ = "1.0.3"
__date__ = "10/2/2025"
__about__ = """
               A customized PySide6 QTabWidget with an 'Add New Tab' button, 'Tab History,' and a 'Tab Search Box.'
                It also features a grey/red tab close button with a hidden tear effect. 
               This was built for use inside a closed-source software, but I am releasing the code as open-source.
            """

def  getpath(filename):
    "returns absolute file path from relative direcory"
    fullapath = Path(__file__).parent.absolute() / Path("images") / Path(filename)
    posixpath = fullapath.as_posix()  # css only support posix path so converting is needed
    return posixpath

class ResizeEventFilter(QObject):
    "this object is used for resize event detction and callback"
    def __init__(self, callback):
        super().__init__()
        self.callback = callback  # Function to call on resizeEvent

    def eventFilter(self, obj, event):
        val = super().eventFilter(obj, event)
        if event.type() == QEvent.Resize:
            self.callback(obj)
        return val

class corner_widget(QWidget):
    "provides few widgets for controlling tab widget"
    def __init__(self,*args, **kargs):
        super().__init__(*args, **kargs)
        self.font = QFont("Arial", 15)
        self.font.setWeight(QFont.Bold)
        self.button = QPushButton("+")
        self.button.setObjectName("newbutton")
        self.button.setFont(self.font)

        self.drop = QPushButton("☰")
        self.drop.setContextMenuPolicy(Qt.CustomContextMenu)
        self.drop.setObjectName("menubutton")

        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(1, 0, 1, 0)
        self.hbox.setSpacing(1)

        self.hbox.addWidget(self.button)
        self.hbox.addWidget(self.drop)
        self.setLayout(self.hbox)
        self.setObjectName("corner_widget")

    def set_newtab_callbacks(self,callbac):
        self.button.clicked.connect(callbac)

    def set_tabhistory_callbacks(self,callbac):
        self.drop.clicked.connect(lambda point=0: callbac(self.drop))

class myTab (QTabWidget):
    """
    it provides some features to tabwidget
    for example a corner widget like  new tab option of firefox
    it will automaticaly resize according to tab height.
    """

    class __style:
        bg = styleconfig.QtabWidget.bg
        border_color = styleconfig.QtabWidget.border_color
        tabbarbg = styleconfig.QtabWidget.tabbarbg
        tabnonfocus = border_color
        tabhovercolor = styleconfig.QtabWidget.tabhovercolor
        tab_height = 35
        tabwidth = 170
        close_image = getpath("close.png")
        close_red_image =  getpath("close_red.png")
        scrollbutton_width = styleconfig.QtabWidget.scrollbutton_width

    def __init__(self, parent=None,*args,show_corner_widget=True,**kargs):
        super().__init__(parent,*args,**kargs)
        self.tabBar().setObjectName("mytabbar")
        self.__corner_widget = corner_widget()
        if show_corner_widget:
              self.__corner_widget.set_newtab_callbacks(self.__new_tab)
              self.__corner_widget.set_tabhistory_callbacks(self.__show_tabhistory_menu)
              self.setCornerWidget(self.__corner_widget, Qt.TopRightCorner)

        self.__set_tab_style()
        self.__eventfilter = ResizeEventFilter(self.__detectresize)

        self.tabBar().installEventFilter(self.__eventfilter)
        self.tabCloseRequested.connect(self.__close_tab)

    def __get_tab_style(self):
        style_sheet = f"""

        {self.objectName()}::pane {{
               border: 1px solid {self.__style.border_color};
               background-color: white;
            }}
        
        #{self.tabBar().objectName()}::tab{{
               border: 1px solid {self.__style.tabnonfocus};
               height:{self.__style.tab_height}px;
               width:{self.__style.tabwidth}px;
               background: {self.__style.bg};
            }}

        #{self.tabBar().objectName()}::tab:hover{{
                  background: {self.__style.tabhovercolor};
            }}

        #{self.tabBar().objectName()}::tab:selected {{
               border: 1px solid {self.__style.border_color};
               background: white;
               color: black;
               border-top: 2px solid blue;
               border-bottom: none;
            }}

        #{self.tabBar().objectName()}::close-button{{
                image: url('{self.__style.close_image}');
            }}

        #{self.tabBar().objectName()}::close-button:hover{{
                image: url('{self.__style.close_red_image}');
            }}
            
        #newbutton {{ 
                border:1px solid {self.__style.border_color};
                height:{ self.tabBar().height()}px;
                width:50px;
                background-color: {self.__style.bg};
            }}

        #newbutton:hover {{
                background-color: {self.__style.tabhovercolor};
            }}
              
        #menubutton {{
                border:1px solid {self.__style.border_color};
                height:{ self.tabBar().height()}px;
                background-color: {self.__style.bg};
                width:50px;
            }}

        #menubutton:hover {{
                background-color: {self.__style.tabhovercolor};
            }}

        #{self.tabBar().objectName()}::tear{{
                image: none;
            }}

        #{self.tabBar().objectName()} QToolButton {{
                border:1px solid {self.__style.border_color};
                background-color: {self.__style.bg};
            }}

        #{self.tabBar().objectName()}::scroller {{
                width:{self.__style.scrollbutton_width};
            }}
        """
        return style_sheet

    def __set_tab_style(self):
        style_sheet = self.__get_tab_style()
        self.setStyleSheet(style_sheet)

    def __new_tab (self, event):
        print("override _myTab__new_tab method to avoid this error ")

    def __detectresize (self, event):
        "when tab bar removed or inserted or size changed dynamicaly then we should resize cornerwidgets. "
        self.__set_tab_style()

    def __close_tab(self, index):
        if self.count()>1:
            self.removeTab(index)

    def __show_tabhistory_menu(self, button=None):
        error = "quick tab history menu is not implemented"
        print( error )


class with_tab_history (myTab):
    "this class provides  tabs history menu for quick tab selection "
    "it provides button for  adding new tab "

    msg = " please override \"_myTab__new_tab\" method of this class to add your own widget when cliking on + icon"

    def _myTab__new_tab (self, event):

        new_tab = QPushButton(self.msg)
        self.addTab(new_tab,f"untitled {self.count()}")
        self.setCurrentWidget(new_tab)
        print(self.msg)

    def _myTab__show_tabhistory_menu(self, button=None):
        "its not exactly a context menu. its a tab history menu."
        context_menu = ScrollableMenu(self)
        for tabindex,text in self.__get_tab():
            action = QAction(text,self)
            action.triggered.connect(lambda placeholder=True, tabindex_number=tabindex:self.__switch_to_tab(tabindex_number))
            context_menu.addAction(action)
        pos = button.rect().bottomRight()
        context_menu.showat(button.mapToGlobal(pos))

    def __get_tab(self):
        "returns tab index and text"
        for onetab in range(self.count()):
            tab_text = self.tabText(onetab)
            yield onetab,tab_text

    def __switch_to_tab(self, tab):
        self.setCurrentIndex(tab)


class WithContextMenu(with_tab_history):
    def __init__(self, parent=None,*args,**kargs):
        super().__init__(parent,*args,**kargs)
        self.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self.__show_context_menu)

    def __show_context_menu(self, pos):
        index = self.tabBar().tabAt(pos)
        if index == -1:
            return  # No tab at this position
        context_menu = CustomQmenu()
        close_action = QAction(QIcon(getpath("close.png")), "close tab", self)
        close_action.triggered.connect(lambda: self._myTab__close_tab(index))
        context_menu.addAction(close_action)
        context_menu.exec(self.tabBar().mapToGlobal(pos))

class with_search_option (WithContextMenu):
    "provides a search bar in conrner widget of tab "
    def __init__(self, *args,**kargs):
        super().__init__(*args,**kargs)
        wid = self.cornerWidget()
        self.__searchbox = search_bar()
        wid.hbox.insertWidget(0, self.__searchbox)
        self.__searchbox.connect_search_box(self.__on_text_changed)
        self.__searchbox.setFocus()

    def _myTab__detectresize(self,evnt):
        super()._myTab__detectresize(evnt)
        self.__searchbox.setStyleSheet(f"""
                #search_box {{ 
                        border:1px solid {styleconfig.QtabWidget.border_color};
                        height:{self.tabBar().size().height()}px;
                        width:120px;
                        background-color: white;
                    }}
                    
                #search_bar {{ 
                        border:1px solid {styleconfig.QtabWidget.border_color};
                        height:{self.tabBar().size().height()}px;
                        width:120px;
                        background-color: white;
                    }}
                
                #search_box:hover {{
                       background-color: {styleconfig.QtabWidget.tabbarbg};
                       }}
                """)
    def __find_matched_tabs (self, text):
        matchd = []
        unmatched = []
        for one_tab in range(self.count()):
            data = self.tabText(one_tab)
            if re.search(text , data):
                matchd.append(one_tab)
            else:
                unmatched.append (one_tab)
        return matchd , unmatched

    def __on_text_changed (self, text=""):
            "search for pattern in tabtext and hides non matched tabs.shows only matched "
            matched,unmatched = self.__find_matched_tabs(text)
            for one_tab in matched:
                self.setTabVisible(one_tab, True)
            for one_tab in unmatched:
                if one_tab == 0 :
                    if len(matched) > 0 :
                        self.setTabVisible(one_tab, False)
                    else:
                        self.setTabVisible(one_tab, True)
                else:
                    self.setTabVisible(one_tab, False)

class search_bar (QWidget):

    def connect_search_box(self,callback):
        self.txt.textChanged.connect(callback)

    def __init__(self,parent=None):
        super().__init__()
        self.setObjectName("search_bar")
        self.ico = QIcon(getpath("find.png"))
        self.txt = QLineEdit()
        self.txt.addAction(self.ico,QLineEdit.TrailingPosition)
        self.txt.setPlaceholderText(" search.. ")
        self.txt.setObjectName("search_box")

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.txt)

        self.hbox.setContentsMargins(1, 0, 1, 0)
        self.hbox.setSpacing(1)
        self.setLayout(self.hbox)

TabPlusPlus = with_search_option # WithContextMenu

if __name__ == "__main__":
    print ( "Qtabwidget test running.." )
    from PySide6.QtWidgets import QApplication, QMainWindow
    import sys
    
    app = QApplication(sys.argv)
    widget = TabPlusPlus(show_corner_widget=True)
    widget.setTabsClosable(True)
    widget.addTab(QPushButton("test button"),"tab 0")
    widget.show()
    sys.exit(app.exec())


