import win32con
import win32gui
import win32ui
from PIL import Image

class Window:
    def __init__(self,
                 title: str,
                 height: int,
                 width: int,
                 showCallable: callable
                 ):
        self.title = title
        self.width = width
        self.height = height
        self.showCallable = showCallable

    def getTitle(self) -> str:
        return self.title

    def getWidth(self) -> int:
        return self.width

    def getHeight(self) -> int:
        return self.height

    def show(self) -> None:
        self.showCallable()

    #TODO: refactor
    def image(self, window_title, output_filename):
        """
            Save the icon of a window to a file

            Args:
                window_title (str): Title of the window to capture (can be partial)
                output_filename (str): Path to save the icon (e.g., 'window_icon.ico')
            """
        # Find the window by title
        hwnd = win32gui.FindWindow(None, window_title)
        if not hwnd:
            raise Exception(f"Window with title '{window_title}' not found")

        # Get the icon
        big_icon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_BIG, 0)
        if not big_icon:
            # Try to get the small icon if big icon isn't available
            big_icon = win32gui.SendMessage(hwnd, win32con.WM_GETICON, win32con.ICON_SMALL, 0)
        if not big_icon:
            # If still no icon, try to get the class icon
            big_icon = win32gui.GetClassLong(hwnd, win32con.GCL_HICON)
        if not big_icon:
            # TODO: add default icon
            raise Exception("No icon found for the window")

        # Create a device context
        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(hwnd))
        hbmp = win32ui.CreateBitmap()
        hbmp.CreateCompatibleBitmap(hdc, 32, 32)
        hdc = hdc.CreateCompatibleDC()
        hdc.SelectObject(hbmp)

        # Draw the icon to the bitmap
        hdc.DrawIcon((0, 0), big_icon)

        bmp_info = hbmp.GetInfo()
        bmp_str = hbmp.GetBitmapBits(True)

        img = Image.frombuffer(
            'RGBA',
            (bmp_info['bmWidth'], bmp_info['bmHeight']),
            bmp_str, 'raw', 'BGRA', 0, 1
        )

        img = img.resize((128, 128))
        # Save as PNG (supports alpha)
        img.save(output_filename, 'PNG')

        # Clean up
        win32gui.DeleteObject(hbmp.GetHandle())
        hdc.DeleteDC()
