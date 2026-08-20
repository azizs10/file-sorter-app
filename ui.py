"""
UI компоненты и управление интерфейсом
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from datetime import datetime
from config import THEMES, SORT_MODES, DEFAULT_CATEGORIES, AVAILABLE_COLORS


class UIBuilder:
    """Класс для построения и управления интерфейсом приложения"""
    
    def __init__(self, app):
        """
        Args:
            app: экземпляр основного приложения FileSorterApp
        """
        self.app = app

    def build_ui(self):
        """Построить весь пользовательский интерфейс"""
        self.app.root.configure(fg_color="#0A0F1A")
        
        # Заголовок
        self._build_header()
        
        # Панель инструментов
        self._build_toolbar()
        
        # Основной контент (левая и правая панели)
        self._build_content()

    def _build_header(self):
        """Построить заголовок приложения"""
        header = ctk.CTkFrame(self.app.root, fg_color="#0F172A", corner_radius=0, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        ctk.CTkLabel(header, text=" FILE SORTER PRO", 
                     font=ctk.CTkFont(family="Courier New", size=24, weight="bold"),
                     text_color="#38BDF8").place(relx=0.5, rely=0.4, anchor="center")
        ctk.CTkLabel(header, text="Advanced file organization tool", 
                     font=ctk.CTkFont(size=12), text_color="#475569").place(relx=0.5, rely=0.75, anchor="center")

    def _build_toolbar(self):
        """Построить панель инструментов"""
        toolbar = ctk.CTkFrame(self.app.root, fg_color="transparent", height=40)
        toolbar.pack(fill="x", padx=20, pady=(10, 0))
        toolbar.pack_propagate(False)
        
        ctk.CTkLabel(toolbar, text="Theme:", font=ctk.CTkFont(size=11), text_color="#64748B").pack(side="left")
        theme_menu = ctk.CTkOptionMenu(toolbar, values=["Dark", "Light", "System"], 
                                       variable=self.app.current_theme, width=100, height=28,
                                       command=self.app.apply_theme)
        theme_menu.pack(side="left", padx=(8, 0))
        
        ctk.CTkButton(toolbar, text="Export Log", font=ctk.CTkFont(size=11), width=90, height=28,
                      fg_color="#1E293B", hover_color="#334155", text_color="#38BDF8",
                      command=self.app.export_log).pack(side="right")

    def _build_content(self):
        """Построить основной контент"""
        content = ctk.CTkFrame(self.app.root, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=15)

        # Левая панель
        left = ctk.CTkFrame(content, fg_color="transparent", width=280)
        left.pack(side="left", fill="y", padx=(0, 15))
        left.pack_propagate(False)

        self._build_left_panel(left)

        # Правая панель
        right = ctk.CTkFrame(content, fg_color="transparent")
        right.pack(side="left", fill="both", expand=True)

        self._build_right_panel(right)

    def _build_left_panel(self, parent):
        """Построить левую панель"""
        # Выбор папки
        folder_frame = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=12)
        folder_frame.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(folder_frame, text="FOLDER TO SORT", 
                     font=ctk.CTkFont(size=10, weight="bold"), text_color="#475569").pack(pady=(12, 6), padx=15, anchor="w")

        self.app.folder_label = ctk.CTkLabel(folder_frame, text="Not selected", 
                                         font=ctk.CTkFont(size=11), text_color="#64748B", wraplength=240, justify="left")
        self.app.folder_label.pack(padx=15, anchor="w")

        self.app.drop_hint = ctk.CTkLabel(folder_frame, text="", font=ctk.CTkFont(size=10), text_color="#475569")
        self.app.drop_hint.pack(padx=15, anchor="w")

        ctk.CTkButton(folder_frame, text="Select folder", font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color="#1E293B", hover_color="#334155", text_color="#38BDF8",
                      corner_radius=8, height=38, command=self.app.pick_folder).pack(fill="x", padx=15, pady=12)

        # Режим сортировки
        mode_frame = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=12)
        mode_frame.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(mode_frame, text="SORT MODE", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color="#475569").pack(pady=(10, 6), padx=15, anchor="w")
        ctk.CTkOptionMenu(mode_frame, values=SORT_MODES, variable=self.app.sort_mode,
                          fg_color="#1E293B", button_color="#334155", button_hover_color="#475569",
                          dropdown_fg_color="#1E293B", dropdown_text_color="#E2E8F0").pack(fill="x", padx=15, pady=(0, 10))

        # Автосортировка
        auto_frame = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=12)
        auto_frame.pack(fill="x", pady=(0, 12))
        ctk.CTkLabel(auto_frame, text="AUTO SORT (minutes)", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color="#475569").pack(pady=(10, 6), padx=15, anchor="w")
        
        self.app.auto_entry = ctk.CTkEntry(auto_frame, placeholder_text="Interval (min)", fg_color="#1E293B",
                                       border_color="#334155", text_color="#E2E8F0")
        self.app.auto_entry.pack(fill="x", padx=15, pady=(0, 6))
        
        self.app.auto_btn = ctk.CTkButton(auto_frame, text="Start Auto-Sort", font=ctk.CTkFont(size=12, weight="bold"),
                                      fg_color="#0369A1", hover_color="#0284C7", height=32,
                                      command=self.app.toggle_auto_sort)
        self.app.auto_btn.pack(fill="x", padx=15, pady=(0, 10))

        # Категории
        cats_frame = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=12)
        cats_frame.pack(fill="both", expand=True)

        cats_header = ctk.CTkFrame(cats_frame, fg_color="transparent")
        cats_header.pack(fill="x", padx=12, pady=(10, 4))
        ctk.CTkLabel(cats_header, text="CATEGORIES", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color="#475569").pack(side="left")
        ctk.CTkButton(cats_header, text="+", font=ctk.CTkFont(size=14, weight="bold"), width=28, height=28,
                      fg_color="#1E293B", hover_color="#334155", text_color="#38BDF8",
                      command=self.app.add_category_dialog).pack(side="right")

        self.app.cats_container = ctk.CTkFrame(cats_frame, fg_color="transparent")
        self.app.cats_container.pack(fill="both", expand=True, padx=6, pady=4)

    def _build_right_panel(self, parent):
        """Построить правую панель"""
        # Статистика
        self.app.stats_frame = ctk.CTkFrame(parent, fg_color="#0F172A", corner_radius=12, height=90)
        self.app.stats_frame.pack(fill="x", pady=(0, 12))
        self.app.stats_frame.pack_propagate(False)

        self.app.stats_label = ctk.CTkLabel(self.app.stats_frame, text="Select a folder to see files",
                                        font=ctk.CTkFont(size=13), text_color="#475569")
        self.app.stats_label.place(relx=0.5, rely=0.5, anchor="center")

        # Заголовок лога
        log_header = ctk.CTkFrame(parent, fg_color="transparent")
        log_header.pack(fill="x")
        ctk.CTkLabel(log_header, text="OPERATION LOG", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color="#475569").pack(side="left")
        ctk.CTkButton(log_header, text="Clear", font=ctk.CTkFont(size=10), fg_color="transparent",
                      hover_color="#1E293B", text_color="#475569", width=60, height=20,
                      command=self.app.clear_log).pack(side="right")

        # Текстовое окно лога
        self.app.log_box = ctk.CTkTextbox(parent, fg_color="#0F172A", text_color="#94A3B8",
                                      font=ctk.CTkFont(family="Courier New", size=11),
                                      corner_radius=12, border_color="#1E293B", border_width=1, wrap="word")
        self.app.log_box.pack(fill="both", expand=True, pady=(6, 12))
        self.app.log_box.configure(state="disabled")

        # Прогресс бар
        self.app.progress = ctk.CTkProgressBar(parent, fg_color="#1E293B", progress_color="#38BDF8",
                                           corner_radius=4, height=6)
        self.app.progress.pack(fill="x", pady=(0, 10))
        self.app.progress.set(0)

        # Кнопка сортировки
        self.app.sort_btn = ctk.CTkButton(parent, text="SORT FILES", font=ctk.CTkFont(size=15, weight="bold"),
                                      fg_color="#0369A1", hover_color="#0284C7", text_color="white",
                                      corner_radius=12, height=50, state="disabled", command=self.app.start_sort)
        self.app.sort_btn.pack(fill="x")

    def apply_theme(self, theme_name):
        """
        Применить тему оформления
        
        Args:
            theme_name: название темы ('Dark', 'Light', 'System')
        """
        theme = THEMES.get(theme_name, THEMES["Dark"])
        ctk.set_appearance_mode(theme["mode"])
        self.app.root.configure(fg_color=theme["bg"])

    def refresh_categories(self):
        """Обновить отображение категорий"""
        for w in self.app.cats_container.winfo_children():
            w.destroy()
        
        for cat_name, cat_data in self.app.category_manager.categories.items():
            row = ctk.CTkFrame(self.app.cats_container, fg_color="transparent")
            row.pack(fill="x", padx=6, pady=2)
            
            ctk.CTkLabel(row, text="●", font=ctk.CTkFont(size=14),
                         text_color=cat_data["color"], width=20).pack(side="left")
            ctk.CTkLabel(row, text=cat_name, font=ctk.CTkFont(size=12),
                         text_color="#94A3B8").pack(side="left", padx=(4, 0))
            
            if cat_name not in DEFAULT_CATEGORIES:
                ctk.CTkButton(row, text="×", font=ctk.CTkFont(size=12), width=20, height=20,
                              fg_color="transparent", hover_color="#1E293B", text_color="#EF4444",
                              command=lambda c=cat_name: self.app.remove_category(c)).pack(side="right")

    def show_add_category_dialog(self):
        """Показать диалог добавления новой категории"""
        dialog = ctk.CTkToplevel(self.app.root)
        dialog.title("New Category")
        dialog.geometry("320x220")
        dialog.configure(fg_color="#0F172A")
        dialog.transient(self.app.root)
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="Category Name", font=ctk.CTkFont(size=12, weight="bold"),
                     text_color="#E2E8F0").pack(pady=(15, 5), padx=20, anchor="w")
        name_entry = ctk.CTkEntry(dialog, fg_color="#1E293B", border_color="#334155", text_color="#E2E8F0")
        name_entry.pack(fill="x", padx=20)

        ctk.CTkLabel(dialog, text="Extensions (comma separated, with dots)",
                     font=ctk.CTkFont(size=11), text_color="#94A3B8").pack(pady=(10, 5), padx=20, anchor="w")
        ext_entry = ctk.CTkEntry(dialog, placeholder_text=".ext1, .ext2", fg_color="#1E293B",
                                 border_color="#334155", text_color="#E2E8F0")
        ext_entry.pack(fill="x", padx=20)

        color_var = ctk.StringVar(value=AVAILABLE_COLORS[0])
        
        ctk.CTkLabel(dialog, text="Color", font=ctk.CTkFont(size=11), text_color="#94A3B8").pack(pady=(10, 5), padx=20, anchor="w")
        color_menu = ctk.CTkOptionMenu(dialog, values=AVAILABLE_COLORS, variable=color_var, width=100)
        color_menu.pack(anchor="w", padx=20)

        def save():
            name = name_entry.get().strip()
            exts = [e.strip() for e in ext_entry.get().split(",") if e.strip()]
            if not name or not exts:
                return
            self.app.category_manager.add_category(name, exts, color_var.get())
            self.refresh_categories()
            dialog.destroy()

        ctk.CTkButton(dialog, text="Add", font=ctk.CTkFont(size=13, weight="bold"),
                      fg_color="#059669", hover_color="#10B981", command=save).pack(pady=15)

    @staticmethod
    def log(app, text, color="#94A3B8"):
        """
        Добавить запись в лог
        
        Args:
            app: экземпляр приложения
            text: текст логирования
            color: цвет текста (не используется в самом CTkTextbox, но может быть полезен)
        """
        def _insert():
            app.log_box.configure(state="normal")
            timestamp = datetime.now().strftime("%H:%M:%S")
            app.log_box.insert("end", f"[{timestamp}] {text}\n")
            app.log_box.configure(state="disabled")
            app.log_box.see("end")
        app.root.after(0, _insert)

    @staticmethod
    def clear_log(app):
        """
        Очистить лог
        
        Args:
            app: экземпляр приложения
        """
        app.log_box.configure(state="normal")
        app.log_box.delete("1.0", "end")
        app.log_box.configure(state="disabled")

    @staticmethod
    def export_log(app):
        """
        Экспортировать лог в файл
        
        Args:
            app: экземпляр приложения
        """
        content = app.log_box.get("1.0", "end").strip()
        if not content:
            messagebox.showinfo("Export", "Log is empty!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if path:
            Path(path).write_text(content, encoding="utf-8")
            UIBuilder.log(app, f"Log exported to: {path}", "#34D399")
