import pygetwindow as gw
from window.Window import Window


class WindowFabric:

    @staticmethod
    def getOpenedWindows() -> list:
        """
            :return: Window[]
        """

        windows = []

        #TODO: refactor
        for window in gw.getAllWindows():
            if window.title and window.title not in [
                "Program Manager",  # Проводник Windows
                "Microsoft Text Input Application",  # Системное окно ввода
                "Default IME",  # Системное окно ввода
                "MSCTFIME UI",  # Системное окно ввода
                "NVIDIA GeForce Overlay",  # Оверлей NVIDIA
                "Windows Input Experience",  # Системное окно
            ] and window.height and window.width:
                windows.append(Window(
                    title=window.title,
                    height=window.height,
                    width=window.width,
                    showCallable=window.restore if window.isMinimized else window.activate
                ))

        return windows