import math

from PyQt6.QtGui import QPainter, QBrush, QColor, QConicalGradient, QPen, QRadialGradient, QLinearGradient
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QWidget, QApplication, QLabel
from PyQt6.QtCore import Qt, QRect, QRectF, QPointF, QPoint, QXmlStreamReader
from math import sin, cos


class RoundSelect(QWidget):
    def __init__(self):
        super().__init__()

        # Устанавливаем прозрачность
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        # Убираем стандартные рамки окна
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # Устанавливаем стиль для прозрачного фона
        self.setStyleSheet("QWidget {background-color: rgba(50, 100, 150, 0.7);}")

        screen = QApplication.primaryScreen()
        self.resize(screen.size().width(), screen.size().height())
        self.setMouseTracking(True)

        self.activeIndex = 0

    def mouseMoveEvent(self, a0, QMouseEvent=None):

        #TODO: refactor

        center = QPoint(self.pos().x() + self.width() // 2, self.pos().y() + self.height() // 2)
        radius = 250
        countParts = 5

        alpha = 360 // countParts

        mousePosition = a0.pos()
        circleRadius = 150

        index = None
        distance = 0

        for i in range(countParts):

            x = radius * cos(math.radians(i * alpha)) + center.x()
            y = radius * sin(math.radians(i * alpha)) + center.y()

            mousePositionDistance = math.sqrt((x - mousePosition.x()) ** 2 + (y - mousePosition.y()) ** 2)

            print(mousePositionDistance)

            if index is None or distance > mousePositionDistance:
                index = i
                distance = mousePositionDistance

        if index != self.activeIndex:
            self.activeIndex = index
            self.repaint()


    #TODO: refactor
    def paintEvent(self, a0, QPaintEvent=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.fillRect(0, 0, self.width(), self.height(), QColor(30, 30, 30, 80))
        painter.setPen(QPen(Qt.PenStyle.NoPen))

        center = QPoint(self.pos().x() + self.width() // 2, self.pos().y() + self.height() // 2)
        radius = 250
        countParts = 5

        alpha = 360 // countParts

        circleRadius = 150

        icon = open("icons/icon.svg", "r")
        svgRenderer = QSvgRenderer(QXmlStreamReader(icon.read()))

        for i in range(countParts):

            x = radius * cos(math.radians(i*alpha)) + center.x()
            y = radius * sin(math.radians(i*alpha)) + center.y()

            gradient = QRadialGradient(x + circleRadius / 2, y + circleRadius / 2, 100)

            if self.activeIndex == i:
                gradient.setColorAt(0.0, QColor(0, 0, 0, 120))
                gradient.setColorAt(1.0, QColor(20, 20, 20, 120))
            else:
                gradient.setColorAt(0.0, QColor(0, 0, 0, 200))
                gradient.setColorAt(1.0, QColor(20, 20, 20, 200))

            painter.setBrush(QBrush(gradient))

            imgX = x + circleRadius / 2 - circleRadius * 0.75 / 2
            imgY = y + circleRadius / 2 - circleRadius * 0.75 / 2

            svgRenderer.render(painter, QRectF(imgX, imgY, circleRadius * 0.75, circleRadius * 0.75))
            painter.drawEllipse(int(x), int(y), circleRadius, circleRadius)

            # label = QLabel("text")
            # label.move(center.x() - label.width() / 2, center.y() - label.height() / 2)

            # painter.drawText(s="text", x=center.x() - label.width() / 2, y=center.y() - label.height() / 2)

        pen = QPen()
        pen.setColor(QColor("white"))

        # label = QLabel("text")
        # label.move(center.x() - label.width() / 2, center.y() - label.height() / 2)

        font = painter.font()
        font.setPixelSize(22)
        painter.setFont(font)
        painter.setPen(pen)
        painter.drawText(center.x(), center.y() + circleRadius // 2, "Hello, world " + str(self.activeIndex))

