import customtkinter as ctk
import os
import shutil
import threading
from pathlib import Path
from tkinter import filedialog
import time
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
CATEGORIES = {
    "🖼️  Изображения": {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff", ".raw"],
        "color": "#FF6B9D",
        "folder": "🖼️ Изображения"
    },
    "📄  Документы": {
        "extensions": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".rtf", ".csv"],
        "color": "#4FC3F7",
        "folder": "📄 Документы"
    },
    "🎵  Музыка": {
        "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
        "color": "#A78BFA",
        "folder": "🎵 Музыка"
    },
    "🎬  Видео": {
        "extensions": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
        "color": "#34D399",
        "folder": "🎬 Видео"
    },
    "💻  Код": {
        "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ts", ".json", ".xml", ".php", ".rb"],
        "color": "#FBBF24",
        "folder": "💻 Код"
    },
    "📦  Архивы": {
        "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "color": "#FB923C",
        "folder": "📦 Архивы"
    },
}
def get_category(ext):
    ext = ext.lower()
    for cat_name, cat_data in CATEGORIES.items():
        if ext in cat_data["extensions"]:
            return cat_name
    return "📂  Другое"
def pick_folder():
    folder = filedialog.askdirectory(title="Выберите папку для сортировки")
    if not folder:
        return
    selected_folder.set(folder)
    short = folder if len(folder) <= 35 else "..." + folder[-32:]
    folder_label.configure(text=short, text_color="#E2E8F0")
    files = [f for f in Path(folder).iterdir() if f.is_file()]
    count = len(files)
    cat_count = {}
    for f in files:
        cat = get_category(f.suffix)
        cat_count[cat] = cat_count.get(cat, 0) + 1
    if count == 0:
        stats_label.configure(text="В папке нет файлов", text_color="#EF4444")
        sort_btn.configure(state="disabled")
        return
    top = sorted(cat_count.items(), key=lambda x: x[1], reverse=True)[:3]
    summary = f"Найдено файлов: {count}   |   " + "   ".join([f"{c}: {n}" for c, n in top])
    stats_label.configure(text=summary, text_color="#38BDF8")
    sort_btn.configure(state="normal")
    log(f"📂 Папка выбрана: {folder}", "#38BDF8")
    log(f"📊 Найдено {count} файлов", "#94A3B8")
def log(text, color="#94A3B8"):
    def _insert():
        log_box.configure(state="normal")
        log_box.insert("end", text + "\n")
        log_box.configure(state="disabled")
        log_box.see("end")
    root.after(0, _insert)
def clear_log():
    log_box.configure(state="normal")
    log_box.delete("1.0", "end")
    log_box.configure(state="disabled")
def start_sort():
    sort_btn.configure(state="disabled", text="⏳  Сортирую...")
    progress.set(0)
    thread = threading.Thread(target=do_sort, daemon=True)
    thread.start()
def do_sort():
    folder = Path(selected_folder.get())
    files = [f for f in folder.iterdir() if f.is_file()]
    if not files:
        log("❌ Файлов не найдено!", "#EF4444")
        root.after(0, lambda: sort_btn.configure(state="normal", text="🚀  СОРТИРОВАТЬ ФАЙЛЫ"))
        return
    moved = 0
    errors = 0
    total = len(files)
    log(f"\n{'─'*40}", "#1E293B")
    log(f"🚀 Начинаю сортировку {total} файлов...", "#FBBF24")
    for i, file_path in enumerate(files):
        try:
            cat_name = get_category(file_path.suffix)
            if cat_name in CATEGORIES:
                cat_folder_name = CATEGORIES[cat_name]["folder"]
                cat_color = CATEGORIES[cat_name]["color"]
            else:
                cat_folder_name = "📂 Другое"
                cat_color = "#94A3B8"
            dest_dir = folder / cat_folder_name
            dest_dir.mkdir(exist_ok=True)
            dest_file = dest_dir / file_path.name
            if dest_file.exists():
                stem = file_path.stem
                suffix = file_path.suffix
                counter = 1
                while dest_file.exists():
                    dest_file = dest_dir / f"{stem}_{counter}{suffix}"
                    counter += 1
            shutil.move(str(file_path), str(dest_file))
            moved += 1
            log(f"  ✓  {file_path.name}  →  {cat_folder_name}", cat_color)
        except Exception as e:
            errors += 1
            log(f"  ✗  {file_path.name}: {e}", "#EF4444")
        progress_val = (i + 1) / total
        root.after(0, lambda v=progress_val: progress.set(v))
        time.sleep(0.05)
    log(f"\n{'─'*40}", "#1E293B")
    log(f"✅ Готово! Перемещено: {moved}  |  Ошибок: {errors}", "#34D399")
    root.after(0, lambda: sort_btn.configure(
        state="normal",
        text="🚀  СОРТИРОВАТЬ ФАЙЛЫ",
        fg_color="#059669",
        hover_color="#10B981"
    ))
    root.after(0, lambda: stats_label.configure(
        text=f"✅ Сортировка завершена! Перемещено {moved} файлов",
        text_color="#34D399"
    ))
root = ctk.CTk()
root.title("📁 Сортировщик файлов")
root.geometry("820x620")
root.configure(fg_color="#0A0F1A")
selected_folder = ctk.StringVar(value="")
header = ctk.CTkFrame(root, fg_color="#0F172A", corner_radius=0, height=80)
header.pack(fill="x")
header.pack_propagate(False)
ctk.CTkLabel(
    header,
    text="📁  СОРТИРОВЩИК ФАЙЛОВ",
    font=ctk.CTkFont(family="Courier New", size=24, weight="bold"),
    text_color="#38BDF8"
).place(relx=0.5, rely=0.45, anchor="center")
ctk.CTkLabel(
    header,
    text="Автоматически раскладывает файлы по папкам",
    font=ctk.CTkFont(size=12),
    text_color="#475569"
).place(relx=0.5, rely=0.78, anchor="center")
content = ctk.CTkFrame(root, fg_color="transparent")
content.pack(fill="both", expand=True, padx=20, pady=15)
left = ctk.CTkFrame(content, fg_color="transparent", width=260)
left.pack(side="left", fill="y", padx=(0, 15))
left.pack_propagate(False)
folder_frame = ctk.CTkFrame(left, fg_color="#0F172A", corner_radius=12)
folder_frame.pack(fill="x", pady=(0, 12))
ctk.CTkLabel(
    folder_frame,
    text="ПАПКА ДЛЯ СОРТИРОВКИ",
    font=ctk.CTkFont(size=10, weight="bold"),
    text_color="#475569"
).pack(pady=(12, 6), padx=15, anchor="w")
folder_label = ctk.CTkLabel(
    folder_frame,
    text="Не выбрана",
    font=ctk.CTkFont(size=11),
    text_color="#64748B",
    wraplength=220,
    justify="left"
)
folder_label.pack(padx=15, anchor="w")
ctk.CTkButton(
    folder_frame,
    text="📂  Выбрать папку",
    font=ctk.CTkFont(size=13, weight="bold"),
    fg_color="#1E293B",
    hover_color="#334155",
    text_color="#38BDF8",
    corner_radius=8,
    height=38,
    command=pick_folder
).pack(fill="x", padx=15, pady=12)
cats_frame = ctk.CTkFrame(left, fg_color="#0F172A", corner_radius=12)
cats_frame.pack(fill="both", expand=True)
ctk.CTkLabel(
    cats_frame,
    text="КАТЕГОРИИ",
    font=ctk.CTkFont(size=10, weight="bold"),
    text_color="#475569"
).pack(pady=(12, 8), padx=15, anchor="w")
for cat_name, cat_data in CATEGORIES.items():
    row = ctk.CTkFrame(cats_frame, fg_color="transparent")
    row.pack(fill="x", padx=12, pady=2)
    ctk.CTkLabel(
        row, text="●",
        font=ctk.CTkFont(size=14),
        text_color=cat_data["color"],
        width=20
    ).pack(side="left")
    ctk.CTkLabel(
        row,
        text=cat_name,
        font=ctk.CTkFont(size=12),
        text_color="#94A3B8"
    ).pack(side="left", padx=(4, 0))
right = ctk.CTkFrame(content, fg_color="transparent")
right.pack(side="left", fill="both", expand=True)
stats_frame = ctk.CTkFrame(right, fg_color="#0F172A", corner_radius=12, height=90)
stats_frame.pack(fill="x", pady=(0, 12))
stats_frame.pack_propagate(False)
stats_label = ctk.CTkLabel(
    stats_frame,
    text="Выберите папку чтобы увидеть файлы",
    font=ctk.CTkFont(size=13),
    text_color="#475569"
)
stats_label.place(relx=0.5, rely=0.5, anchor="center")
log_header = ctk.CTkFrame(right, fg_color="transparent")
log_header.pack(fill="x")
ctk.CTkLabel(
    log_header,
    text="ЛОГ ОПЕРАЦИЙ",
    font=ctk.CTkFont(size=10, weight="bold"),
    text_color="#475569"
).pack(side="left")
ctk.CTkButton(
    log_header,
    text="Очистить",
    font=ctk.CTkFont(size=10),
    fg_color="transparent",
    hover_color="#1E293B",
    text_color="#475569",
    width=60, height=20,
    command=clear_log
).pack(side="right")
log_box = ctk.CTkTextbox(
    right,
    fg_color="#0F172A",
    text_color="#94A3B8",
    font=ctk.CTkFont(family="Courier New", size=11),
    corner_radius=12,
    border_color="#1E293B",
    border_width=1,
    wrap="word"
)
log_box.pack(fill="both", expand=True, pady=(6, 12))
log_box.configure(state="disabled")
progress = ctk.CTkProgressBar(
    right,
    fg_color="#1E293B",
    progress_color="#38BDF8",
    corner_radius=4,
    height=6
)
progress.pack(fill="x", pady=(0, 10))
progress.set(0)
sort_btn = ctk.CTkButton(
    right,
    text="🚀  СОРТИРОВАТЬ ФАЙЛЫ",
    font=ctk.CTkFont(size=15, weight="bold"),
    fg_color="#0369A1",
    hover_color="#0284C7",
    text_color="white",
    corner_radius=12,
    height=50,
    state="disabled",
    command=start_sort
)
sort_btn.pack(fill="x")
root.mainloop()
