from PySide6.QtWidgets import  QMenu
from PySide6 import QtGui
from PySide6 import QtCore
import styleconfig


class CustomQmenu(QMenu):
    """
    this menu looks more beautifull than pyside6 default qmenu.
    it also canbe used instead of pyside6 qmenu because all methods and attributes are available
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.radius = 10
        self.setStyleSheet(self.__get_qmenu_style())

    def __get_qmenu_style(self):
        return f"""
                    QMenu {{
                        background-color: #ffffff;
                        border: 2px solid {styleconfig.Qmenu.border_color};
                        border-radius: {self.radius}px; 
                        padding: 5px;
                        }}
                    QMenu::item {{
                        padding: 5px 15px;
                        border-radius: 5px;  
                        }}
                    QMenu::item:selected {{
                        background-color: {styleconfig.Qmenu.selection_color};  
                        color: white;  
                        }}
                """
    def resizeEvent(self, event):
        "this is needed to make edges round.otherwise it will show a black mark on bottm right corner"
        path = QtGui.QPainterPath()
        rect = QtCore.QRectF(self.rect()).adjusted(0.0, 0.0, -0.0, -0.0)
        path.addRoundedRect(rect, self.radius, self.radius)
        region = QtGui.QRegion(path.toFillPolygon(QtGui.QTransform()).toPolygon())
        self.setMask(region)
        super().resizeEvent(event)


if __name__ == "__main__":
    print("Qmenu test running..")
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import  QAction
    import sys

    app = QApplication(sys.argv)
    context_menu = CustomQmenu()
    all = []
    for x in range(1,10):
        close_action = QAction(f"test {x}")
        close_action.triggered.connect(lambda y,selected=x:( print("it's working, selected" ,selected),sys.exit()))
        all.append(close_action)
        context_menu.addAction(close_action)
    context_menu.exec(QPoint(300,300))

    sys.exit()
