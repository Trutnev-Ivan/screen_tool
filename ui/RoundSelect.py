import math
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen, QRadialGradient
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRectF, QPoint, QXmlStreamReader
from math import sin, cos
import os.path


class RoundSelect(QWidget):
    def __init__(self,
                 radius=250,
                 elemRadius=150,
                 elems=[]
                 ):
        """
        :param int radius:
            radius from center elements; display how far circles placed from center
        :param int elemRadius:
            radius of circle element
        :param dict[] elems:
            description of circle element in format
            {
                "title" -> str, # display text title of element
                "active" -> bool, # is active by default
                "icon" -> str, # svg icon for elem circle
            }
        """
        super().__init__()

        self.radius = int(radius) if radius > 0 else 250
        self.elemRadius = int(elemRadius) if elemRadius > 0 else 150
        self.elems = elems

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

        for i, elem in enumerate(self.elems):
            if "active" in elem and elem["active"]:
                self.activeIndex = i
                break

    # Обновляем текущий элемент при наведении на него мышью
    def mouseMoveEvent(self, a0, QMouseEvent=None):
        center = QPoint(self.pos().x() + self.width() // 2, self.pos().y() + self.height() // 2)
        countParts = len(self.elems)

        alpha = 360 // countParts
        degreeOffset = 180

        mousePosition = a0.pos()

        index = None
        distance = 0

        for i in range(countParts):

            x = self.radius * cos(math.radians(i * alpha + degreeOffset)) + center.x()
            y = self.radius * sin(math.radians(i * alpha + degreeOffset)) + center.y()

            mousePositionDistance = math.sqrt((x - mousePosition.x()) ** 2 + (y - mousePosition.y()) ** 2)

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
        countParts = len(self.elems)

        alpha = 360 // countParts
        degreeOffset = 180

        for i in range(countParts):

            if "icon" in self.elems[i] and os.path.exists(self.elems[i]["icon"]) and self.elems[i]["icon"].endswith(".svg"):
                icon = open(self.elems[i]["icon"], "r")
            else:
                icon = open("icons/default.svg", "r")

            svgRenderer = QSvgRenderer(QXmlStreamReader(icon.read()))

            x = self.radius * cos(math.radians(i*alpha + degreeOffset)) + center.x()
            y = self.radius * sin(math.radians(i*alpha + degreeOffset)) + center.y()

            gradient = QRadialGradient(
                x + self.elemRadius / 2,
                y + self.elemRadius / 2,
                100)

            if self.activeIndex == i:
                gradient.setColorAt(0.0, QColor(0, 0, 0, 120))
                gradient.setColorAt(1.0, QColor(20, 20, 20, 120))
            else:
                gradient.setColorAt(0.0, QColor(0, 0, 0, 200))
                gradient.setColorAt(1.0, QColor(20, 20, 20, 200))

            painter.setBrush(QBrush(gradient))

            imgX = x + self.elemRadius / 2 - self.elemRadius * 0.75 / 2
            imgY = y + self.elemRadius / 2 - self.elemRadius * 0.75 / 2

            svgRenderer.render(painter, QRectF(imgX, imgY, self.elemRadius * 0.75, self.elemRadius * 0.75))
            painter.drawEllipse(int(x), int(y), self.elemRadius, self.elemRadius)

        pen = QPen()
        pen.setColor(QColor("white"))

        font = painter.font()
        font.setPixelSize(22)
        painter.setFont(font)
        painter.setPen(pen)
        painter.drawText(
            center.x(),
            center.y() + self.elemRadius // 2,
            str(self.elems[self.activeIndex]["title"])
        )

