"""
Конфигурация и константы приложения File Sorter Pro
"""
from pathlib import Path

# Масштабирование интерфейса
WIDGET_SCALING = 1.4
WINDOW_SCALING = 1.4

# Темы оформления
THEMES = {
    "Dark": {"mode": "dark", "bg": "#0A0F1A", "card": "#0F172A", "text": "#E2E8F0", "muted": "#94A3B8"},
    "Light": {"mode": "light", "bg": "#F1F5F9", "card": "#FFFFFF", "text": "#0F172A", "muted": "#64748B"},
    "System": {"mode": "system", "bg": "#0A0F1A", "card": "#0F172A", "text": "#E2E8F0", "muted": "#94A3B8"}
}

# Файл настроек
SETTINGS_FILE = Path.home() / ".file_sorter_settings.json"

# Категории по умолчанию
DEFAULT_CATEGORIES = {
    "Images": {
        "extensions": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico", ".tiff", ".raw"],
        "color": "#FF6B9D",
        "folder": "Images"
    },
    "Documents": {
        "extensions": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".rtf", ".csv"],
        "color": "#4FC3F7",
        "folder": "Documents"
    },
    "Music": {
        "extensions": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"],
        "color": "#A78BFA",
        "folder": "Music"
    },
    "Video": {
        "extensions": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
        "color": "#34D399",
        "folder": "Video"
    },
    "Code": {
        "extensions": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".ts", ".json", ".xml", ".php", ".rb"],
        "color": "#FBBF24",
        "folder": "Code"
    },
    "Archives": {
        "extensions": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
        "color": "#FB923C",
        "folder": "Archives"
    },
}

# Режимы сортировки
SORT_MODES = ["By Extension", "By Date", "By Size"]

# Цвета для новых категорий
AVAILABLE_COLORS = ["#FF6B9D", "#4FC3F7", "#A78BFA", "#34D399", "#FBBF24", "#FB923C", "#EF4444", "#22D3EE"]
