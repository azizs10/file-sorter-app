"""
Drag & Drop функциональность для Windows
"""
import os
import ctypes
from ctypes import wintypes


class DragDropHelper:
    """Класс для реализации Drag & Drop функциональности на Windows"""
    
    def __init__(self, widget, callback):
        """
        Args:
            widget: tkinter виджет для приёма файлов
            callback: функция обратного вызова при проводке файла
        """
        self.widget = widget
        self.callback = callback
        self._setup()

    def _setup(self):
        """Регистрируем окно для приёма файлов и подменяем оконную процедуру"""
        # Получаем дескриптор окна
        hwnd = ctypes.windll.user32.GetParent(self.widget.winfo_id())
        # Регистрируем окно для приёма файлов
        ctypes.windll.shell32.DragAcceptFiles(hwnd, True)
        
        # Подменяем оконную процедуру
        self.old_wndproc = ctypes.windll.user32.GetWindowLongPtrW(hwnd, -4)
        prototype = ctypes.WINFUNCTYPE(wintypes.LPARAM, wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM)
        self.new_wndproc = prototype(self._wndproc)
        ctypes.windll.user32.SetWindowLongPtrW(hwnd, -4, self.new_wndproc)
        self.hwnd = hwnd

    def _wndproc(self, hwnd, msg, wparam, lparam):
        """Обработчик оконных событий"""
        WM_DROPFILES = 0x0233
        if msg == WM_DROPFILES:
            hdrop = wparam
            # Получаем количество файлов
            file_count = ctypes.windll.shell32.DragQueryFileW(hdrop, 0xFFFFFFFF, None, 0)
            for i in range(file_count):
                buf = ctypes.create_unicode_buffer(260)
                ctypes.windll.shell32.DragQueryFileW(hdrop, i, buf, 260)
                path = buf.value
                # Обрабатываем только папки
                if os.path.isdir(path):
                    self.widget.after(10, lambda p=path: self.callback(p))
                    break
            ctypes.windll.shell32.DragFinish(hdrop)
            return 0
        return ctypes.windll.user32.CallWindowProcW(self.old_wndproc, hwnd, msg, wparam, lparam)
