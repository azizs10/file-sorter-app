"""
Управление категориями файлов
"""
import json
from pathlib import Path
from config import SETTINGS_FILE, DEFAULT_CATEGORIES


class CategoryManager:
    """Менеджер для работы с категориями файлов"""
    
    def __init__(self):
        """Инициализация менеджера категорий"""
        self.categories = {}
        self.load_settings()

    def load_settings(self):
        """Загружает категории из файла настроек"""
        if SETTINGS_FILE.exists():
            try:
                data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
                self.categories = data.get("categories", {})
            except Exception:
                self.categories = {}
        if not self.categories:
            self.categories = {k: dict(v) for k, v in DEFAULT_CATEGORIES.items()}

    def save_settings(self):
        """Сохраняет категории в файл настроек"""
        data = {"categories": self.categories}
        SETTINGS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_category(self, ext):
        """
        Получает категорию по расширению файла
        
        Args:
            ext: расширение файла (например, '.jpg')
            
        Returns:
            Название категории или "Other"
        """
        ext = ext.lower()
        for cat_name, cat_data in self.categories.items():
            if ext in cat_data["extensions"]:
                return cat_name
        return "Other"

    def add_category(self, name, extensions, color):
        """
        Добавляет новую категорию
        
        Args:
            name: название категории
            extensions: список расширений
            color: цвет категории (hex)
        """
        self.categories[name] = {
            "extensions": extensions,
            "color": color,
            "folder": name
        }
        self.save_settings()

    def remove_category(self, name):
        """
        Удаляет пользовательскую категорию (не трогает встроенные)
        
        Args:
            name: название категории для удаления
        """
        if name in self.categories and name not in DEFAULT_CATEGORIES:
            del self.categories[name]
            self.save_settings()
