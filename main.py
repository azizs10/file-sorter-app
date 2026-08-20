"""
File Sorter Pro - главный модуль приложения
"""
import customtkinter as ctk
import threading
from pathlib import Path
from tkinter import filedialog, messagebox

from config import WIDGET_SCALING, WINDOW_SCALING, SORT_MODES, DEFAULT_CATEGORIES
from drag_drop import DragDropHelper
from categories import CategoryManager
from sorter import FileSorter
from ui import UIBuilder


class FileSorterApp:
    """Главное приложение File Sorter Pro"""
    
    def __init__(self, root):
        """
        Инициализация приложения
        
        Args:
            root: главное окно Tkinter (CTk)
        """
        self.root = root
        self.root.title("File Sorter Pro")
        self.root.geometry("900x720")
        
        # Инициализация компонентов
        self.category_manager = CategoryManager()
        self.ui_builder = UIBuilder(self)
        self.file_sorter = FileSorter(
            self.category_manager,
            self._update_progress,
            self._log
        )
        
        # Переменные состояния
        self.selected_folder = ctk.StringVar(value="")
        self.sort_mode = ctk.StringVar(value=SORT_MODES[0])
        self.current_theme = ctk.StringVar(value="Dark")
        
        self.auto_sort_active = False
        self.auto_sort_timer = None
        
        # Построение интерфейса
        self.ui_builder.build_ui()
        self.ui_builder.apply_theme("Dark")
        self.ui_builder.refresh_categories()
        
        # Инициализация Drag & Drop
        self._setup_drag_drop()

    def _setup_drag_drop(self):
        """Настроить функциональность Drag & Drop"""
        try:
            self.dnd = DragDropHelper(self.root, self.on_folder_dropped)
            self.drop_hint.configure(text="Or drag & drop folder here")
        except Exception:
            self.drop_hint.configure(text="Drag & Drop unavailable")

    # ───────────────────────────────────────────────────
    # УПРАВЛЕНИЕ ПАПКАМИ И ИНФОРМАЦИЕЙ
    # ───────────────────────────────────────────────────

    def pick_folder(self):
        """Открыть диалог выбора папки"""
        folder = filedialog.askdirectory(title="Select folder to sort")
        if not folder:
            return
        self.selected_folder.set(folder)
        self.update_folder_info()

    def on_folder_dropped(self, path):
        """Обработать проброс папки через Drag & Drop"""
        self.selected_folder.set(path)
        self.update_folder_info()

    def update_folder_info(self):
        """Обновить информацию о выбранной папке"""
        folder = self.selected_folder.get()
        short = folder if len(folder) <= 35 else "..." + folder[-32:]
        self.folder_label.configure(text=short, text_color="#E2E8F0")

        files = [f for f in Path(folder).iterdir() if f.is_file()]
        count = len(files)

        cat_count = {}
        for f in files:
            cat = self.category_manager.get_category(f.suffix)
            cat_count[cat] = cat_count.get(cat, 0) + 1

        if count == 0:
            self.stats_label.configure(text="No files in folder", text_color="#EF4444")
            self.sort_btn.configure(state="disabled")
            return

        top = sorted(cat_count.items(), key=lambda x: x[1], reverse=True)[:3]
        summary = f"Found files: {count}   |   " + "   ".join([f"{c}: {n}" for c, n in top])
        self.stats_label.configure(text=summary, text_color="#38BDF8")
        self.sort_btn.configure(state="normal")

        self._log(f"Folder selected: {folder}", "#38BDF8")
        self._log(f"Found {count} files", "#94A3B8")

    # ───────────────────────────────────────────────────
    # УПРАВЛЕНИЕ КАТЕГОРИЯМИ
    # ───────────────────────────────────────────────────

    def add_category_dialog(self):
        """Показать диалог добавления новой категории"""
        self.ui_builder.show_add_category_dialog()

    def remove_category(self, name):
        """Удалить категорию"""
        self.category_manager.remove_category(name)
        self.ui_builder.refresh_categories()

    # ───────────────────────────────────────────────────
    # УПРАВЛЕНИЕ ТЕМАМИ
    # ───────────────────────────────────────────────────

    def apply_theme(self, theme_name):
        """Применить тему оформления"""
        self.ui_builder.apply_theme(theme_name)

    # ───────────────────────────────────────────────────
    # ЛОГИРОВАНИЕ
    # ───────────────────────────────────────────────────

    def _log(self, text, color="#94A3B8"):
        """Добавить запись в лог"""
        UIBuilder.log(self, text, color)

    def clear_log(self):
        """Очистить лог"""
        UIBuilder.clear_log(self)

    def export_log(self):
        """Экспортировать лог в файл"""
        UIBuilder.export_log(self)

    # ───────────────────────────────────────────────────
    # СОРТИРОВКА ФАЙЛОВ
    # ───────────────────────────────────────────────────

    def start_sort(self):
        """Начать сортировку в отдельном потоке"""
        self.sort_btn.configure(state="disabled", text=" Sorting...")
        self.progress.set(0)
        thread = threading.Thread(target=self.do_sort, daemon=True)
        thread.start()

    def do_sort(self):
        """Выполнить сортировку (работает в отдельном потоке)"""
        folder = self.selected_folder.get()
        mode = self.sort_mode.get()

        try:
            if mode == "By Extension":
                moved, errors = self.file_sorter.sort_by_extension(folder)
            elif mode == "By Date":
                moved, errors = self.file_sorter.sort_by_date(folder)
            elif mode == "By Size":
                moved, errors = self.file_sorter.sort_by_size(folder)
            else:
                moved, errors = 0, 1
                self._log("Unknown sort mode!", "#EF4444")

            # Обновляем UI в главном потоке
            self.root.after(0, lambda: self._update_sort_complete(moved, errors))

        except Exception as e:
            self._log(f"Sorting error: {e}", "#EF4444")
            self.root.after(0, self._reset_sort_button)

    def _update_progress(self, value):
        """Обновить прогресс (вызывается из потока сортировки)"""
        self.root.after(0, lambda: self.progress.set(value))

    def _update_sort_complete(self, moved, errors):
        """Обновить UI после завершения сортировки"""
        self.sort_btn.configure(state="normal", text="SORT FILES", fg_color="#0369A1", hover_color="#0284C7")
        self.stats_label.configure(
            text=f"Sorting complete! Moved {moved} files",
            text_color="#34D399"
        )

    def _reset_sort_button(self):
        """Сбросить кнопку сортировки в исходное состояние"""
        self.sort_btn.configure(state="normal", text="SORT FILES", fg_color="#0369A1", hover_color="#0284C7")

    # ───────────────────────────────────────────────────
    # АВТОСОРТИРОВКА
    # ───────────────────────────────────────────────────

    def toggle_auto_sort(self):
        """Включить/отключить автосортировку"""
        if self.auto_sort_active:
            self.auto_sort_active = False
            if self.auto_sort_timer:
                self.auto_sort_timer.cancel()
            self.auto_btn.configure(text="Start Auto-Sort", fg_color="#0369A1", hover_color="#0284C7")
            self._log("Auto-sort stopped", "#EF4444")
        else:
            try:
                minutes = float(self.auto_entry.get())
                if minutes <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Auto-Sort", "Enter a valid interval in minutes!")
                return
            
            if not self.selected_folder.get():
                messagebox.showwarning("Auto-Sort", "Select a folder first!")
                return

            self.auto_sort_active = True
            self.auto_btn.configure(text="Stop Auto-Sort", fg_color="#EF4444", hover_color="#DC2626")
            self._log(f"Auto-sort started: every {minutes} min", "#34D399")
            self.schedule_auto_sort(minutes)

    def schedule_auto_sort(self, minutes):
        """Запланировать следующую автосортировку"""
        if not self.auto_sort_active:
            return
        self.start_sort()
        self.auto_sort_timer = threading.Timer(
            minutes * 60,
            lambda: self.schedule_auto_sort(minutes)
        )
        self.auto_sort_timer.daemon = True
        self.auto_sort_timer.start()


# ═══════════════════════════════════════════════════════════════
# ЗАПУСК ПРИЛОЖЕНИЯ
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Инициализация customtkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    ctk.set_widget_scaling(WIDGET_SCALING)
    ctk.set_window_scaling(WINDOW_SCALING)
    
    # Создание и запуск главного окна
    root = ctk.CTk()
    app = FileSorterApp(root)
    root.mainloop()
