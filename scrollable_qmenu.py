from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QScrollArea, QFrame
from PySide6.QtGui import QFont,QAction,QIcon
from qmenu import CustomQmenu as QMenu
from PySide6.QtCore import QPoint

"""
ai generated code for pyside6 scrollable qmenu
"""

class ScrollableMenu(QMenu):
    def __init__(self,*args,**kargs):
        super().__init__(*args,**kargs)
        self.hover_color = "#f1f1f1"
        # Create Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        # Create a container widget for menu items
        self.menu_container = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setSpacing(0)

        self.scroll.setWidget(self.menu_container)
        self.setLayout(QVBoxLayout())  # Menu layout
        self.layout().addWidget(self.scroll)

    def addAction(self, action,hover_color=None):
        """Override addAction to insert into the scrollable area"""
        if hover_color == None:
            hover_color = self.hover_color
        btn = QPushButton(action.text())
        btn.clicked.connect(action.triggered.emit)  # Link button to action
        btn.setFlat(True)  # Make it look like a menu item
        btn.setObjectName("addbutton")
        btn.setStyleSheet(f"""#addbutton {{
                                 text-align: left;
                                 border: 0px solid red;
                                 padding: 5px;
                                 background-color:white;
                                 }}
                            #addbutton:hover {{
                                background-color: {hover_color};
                                color : black;
                                }}

                            """)
        self.menu_layout.addWidget(btn)

    def showEvent(self, event):
        """Adjust menu size on show"""
        self.menu_container.adjustSize()
        self.scroll.setFixedSize(self.menu_container.sizeHint().width() + 20,
                                 min(400, self.menu_container.sizeHint().height()))
        super().showEvent(event)

    def showat(self,pos,padding=10):
        screen_rect = QApplication.primaryScreen().geometry()
        btn_global_pos = pos

        # Calculate the best position to keep the menu inside the screen
        menu_width = self.width()
        menu_height = self.scroll.height()

        x = btn_global_pos.x()
        y = btn_global_pos.y()

        # Prevent menu from going off-screen (right edge)
        if x + menu_width > screen_rect.right():
            x = screen_rect.right() - menu_width -padding

        if y + menu_height > screen_rect.bottom():
            y = btn_global_pos.y() - menu_height-padding

        self.exec(QPoint(x,y))


class MyWindow(QWidget):
    def print(self,x=""):
        print(x)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Create a button to open the menu
        self.menu_button = QPushButton("Open Menu")
        layout.addWidget(self.menu_button)

        # Create scrollable menu
        self.menu = ScrollableMenu("Scrollable Menu", self)

        # Add many items to show scrollbar effect
        for i in range(1520):
            action = QAction(f"Option {i + 1}", self)
            action.triggered.connect(self.print)
            self.menu.addAction(action)

        # Connect button to open menu
        self.menu_button.setMenu(self.menu)

        self.setLayout(layout)
        self.setWindowTitle("QMenu with Scrollbar")


# Run application
if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()
