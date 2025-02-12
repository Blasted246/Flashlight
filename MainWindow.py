import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRect, QPoint, QTimer, QTime

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.last_frame_time = QTime.currentTime()
        self.square_size = 50
        self.dragging = False
        self.transparent = False
        self.square_x = (self.screen().size().width() / 2) - (self.square_size / 2)
        self.square_y = (self.screen().size().height() / 2) - (self.square_size / 2)
        self.setStyleSheet("background-color: black;")
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setAttribute(Qt.WA_AlwaysStackOnTop)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showFPS)
        self.timer.start(1000)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawSquare(qp)
        qp.end()
    def drawSquare(self, qp):
        brush = QBrush(QColor(255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        qp.setPen(QPen(Qt.NoPen))
        qp.setBrush(brush)
        qp.drawRect(QRect(int(self.square_x), int(self.square_y), int(self.square_size), int(self.square_size)))
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.start_drag_x = event.x() - self.square_x
            self.start_drag_y = event.y() - self.square_y

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.square_x = event.x() - self.start_drag_x
            self.square_y = event.y() - self.start_drag_y
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def wheelEvent(self, event):
        num_degrees = event.angleDelta().y() / 8
        num_steps = num_degrees / 15
        self.square_size += num_steps
        self.update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.square_x = (self.screen().size().width() / 2) - (self.square_size / 2)
            self.square_y = (self.screen().size().height() / 2) - (self.square_size / 2)
            self.update()

        if event.key() == Qt.Key_F:
            if self.transparent:
                self.setAttribute(Qt.WA_TranslucentBackground, False)
                self.setStyleSheet("background-color: black;")
            else:
                self.setAttribute(Qt.WA_TranslucentBackground, True)
                self.setStyleSheet("background-color: transparent;")
            self.transparent = not self.transparent

        if event.key() == Qt.Key_Escape:
            self.close()

    def showFPS(self):
        current_time = QTime.currentTime()

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

