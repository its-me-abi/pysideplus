
from PySide6.QtWidgets import ( QApplication,
                               QTabWidget, QWidget, QPushButton,
                               QTabBar,QSizePolicy,QLabel,QHBoxLayout,
                               QVBoxLayout,QMenu,QSpacerItem , QMessageBox,
                               QGraphicsDropShadowEffect
                                )
from PySide6.QtCore import Qt,Signal,QSize,QObject, QEvent,QPoint
from PySide6.QtGui import QFont,QPainter, QColor,QAction,QIcon
from api import styleconfig
from pathlib import Path


__author__ = "github.com/its-me-abilash"
__version__ = "1.0.2"
__date__ = "2/2/2025"
__about__ = """
               customized pyside6 QTabWidget with 'add new tab' and 'tab history ' and few more  features.
               it also has grey/red tab closebutton with hidden tear . this is built for using inside a closed source software
               but iam releasing this code as opensource.
            """

def  getpath(filename):
    "returns absolute file path from relative direcory"
    fullapath = Path(__file__).parent.absolute() / Path("images") / Path(filename)
    posixpath = fullapath.as_posix()  # css only support posix path so converting is needed
    return posixpath

class ResizeEventFilter(QObject):
    "this object is used for resize event deetction and callback"
    def __init__(self, callback):
        super().__init__()
        self.callback = callback  # Function to call on resizeEvent

    def eventFilter(self, obj, event):
        val = super().eventFilter(obj, event)
        if event.type() == QEvent.Resize:
            self.callback(obj)
        return val


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
        if show_corner_widget:
              self.__corner_widget = self.__create_corner_widget()
              self.setCornerWidget(self.__corner_widget, Qt.TopRightCorner)
        self.__set_tab_style()
        self.__eventfilter = ResizeEventFilter(self.__detectresize)

        self.tabBar().installEventFilter(self.__eventfilter)
        self.tabCloseRequested.connect(self.__close_tab)

    def __get_tab_style(self):
        style_sheet = f"""

        {self.objectName()}::pane {{
               border: 1px solid {self.__style.border_color};
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
        raise NotImplementedError("override __new_tab method")

    def __detectresize (self, event):
        "when tab bar removed or inserted or size changed dynamicaly then we should resize cornerwidgets. "
        self.__set_tab_style()

    def __create_corner_widget (self):
        font = QFont("Arial", 15)
        font.setWeight(QFont.Bold)
        button = QPushButton("+")
        button.setObjectName("newbutton")
        button.clicked.connect(self.__new_tab)
        button.setFont(font)

        drop = QPushButton("☰")
        drop.setContextMenuPolicy(Qt.CustomContextMenu)
        drop.clicked.connect(lambda point=0,button=drop:self.__show_tabhistory_menu(button))
        drop.setObjectName("menubutton")

        corner_widget = QWidget()
        corner_widget.setObjectName("corner_widget")

        hbox =  QHBoxLayout(corner_widget)
        hbox.setContentsMargins(1, 0, 1, 0)
        hbox.setSpacing(1)

        hbox.addWidget( button )
        hbox.addWidget( drop )

        corner_widget.setLayout(hbox)
        return corner_widget

    def __close_tab(self, index):
        if self.count()>1:
            self.removeTab(index)

    def __show_tabhistory_menu(self, button=None):
        error = "quick tab history menu is not implemented"
        raise NotImplementedError(error)


class with_tab_history (myTab):
    "this class provides  tabs history menu for quick tab selection "
    "it also provides button for  adding new tab "

    msg = " please override \"_myTab__new_tab\" method of this class to add your own widget when cliking on + icon"

    def _myTab__new_tab (self, event):

        new_tab = QPushButton(self.msg)
        self.addTab(new_tab,f"untitled {self.count()}")
        self.setCurrentWidget(new_tab)
        raise NotImplementedError(self.msg)

    def __get_history_style(self):
        return    """
                   QMenu {
                       border: 2px solid #D1D5DB;
                       border-radius: 5px;        
                       background-color: white;   
                   }
                   QMenu::item {
                       padding: 5px 20px;        
                   }
                   QMenu::item:selected {
                       background-color: #0078d7;   
                       color: white; 
                   }
                   """
    def _myTab__show_tabhistory_menu(self, button=None):
        "its not exactly a context menu. its a tab history menu."
        context_menu = QMenu(self)
        context_menu.setStyleSheet(self.__get_history_style())

        for tabindex,text in self.__get_tab():
            action = QAction(text,self)
            action.triggered.connect(lambda placeholder=True, tabindex_number=tabindex:self.__switch_to_tab(tabindex_number))
            context_menu.addAction(action)
        pos = button.rect().bottomRight()
        context_menu.exec(button.mapToGlobal(pos))

    def __get_tab(self):
        "returns tab index and text"
        for onetab in range(self.count()):
            tab_text = self.tabText(onetab)
            yield onetab,tab_text

    def __switch_to_tab(self, tab):
        self.setCurrentIndex(tab)


class WithContextMenu(with_tab_history):

    class __style:
        Qmenuborder_color = styleconfig.Qmenu.border_color
        Qmenu_selection_color =  styleconfig.Qmenu.selection_color

    def __init__(self, parent=None,*args,**kargs):
        super().__init__(parent,*args,**kargs)
        self.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self.show_context_menu)

    def __get_qmenu_style(self):
        return f"""
                    QMenu {{
                        background-color: #ffffff;
                        border: 1px solid {self.__style.Qmenuborder_color};
                        border-radius: 10px; 
                        padding: 5px;
                        }}
                    QMenu::item {{
                        padding: 5px 15px;
                        border-radius: 5px;  
                        }}
                    QMenu::item:selected {{
                        background-color: {self.__style.Qmenu_selection_color};  
                        color: white;  
                        }}
                """

    def show_context_menu(self, pos):
        index = self.tabBar().tabAt(pos)
        if index == -1:
            return  # No tab at this position
        context_menu = QMenu()
        context_menu.setStyleSheet(self.__get_qmenu_style())
        close_action = QAction(QIcon(getpath("close.png")), "close tab", self)
        close_action.triggered.connect(lambda: self._myTab__close_tab(index))
        context_menu.addAction(close_action)
        context_menu.exec(self.tabBar().mapToGlobal(pos))


TabPlusPlus = WithContextMenu

if __name__ == "__main__":
    print ( "test running" )
    from PySide6.QtWidgets import QApplication, QMainWindow
    import sys
    
    app = QApplication(sys.argv)
    widget = TabPlusPlus(show_corner_widget=True)
    widget.setTabsClosable(True)
    widget.addTab(QPushButton("button"),"tab 0")
    widget.show()
    sys.exit(app.exec())


