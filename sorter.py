"""
Логика сортировки файлов
"""
import shutil
import time
import threading
from pathlib import Path
from datetime import datetime


class FileSorter:
    """Класс для сортировки файлов"""
    
    def __init__(self, category_manager, progress_callback, log_callback):
        """
        Args:
            category_manager: экземпляр CategoryManager
            progress_callback: функция обратного вызова для прогресса (0-1)
            log_callback: функция обратного вызова для логирования
        """
        self.category_manager = category_manager
        self.progress_callback = progress_callback
        self.log_callback = log_callback

    def sort_by_extension(self, folder_path):
        """
        Сортирует файлы по типам (расширениям)
        
        Args:
            folder_path: путь к папке для сортировки
            
        Returns:
            Кортеж (количество перемещённых, количество ошибок)
        """
        folder = Path(folder_path)
        files = [f for f in folder.iterdir() if f.is_file()]
        
        if not files:
            self.log_callback("No files found!", "#EF4444")
            return 0, 0

        moved = 0
        errors = 0
        total = len(files)

        self.log_callback(f"\n{'─'*40}", "#1E293B")
        self.log_callback(f"Starting sorting {total} files (By Extension)...", "#FBBF24")

        for i, file_path in enumerate(files):
            try:
                cat_name = self.category_manager.get_category(file_path.suffix)
                if cat_name in self.category_manager.categories:
                    cat_folder_name = self.category_manager.categories[cat_name]["folder"]
                    cat_color = self.category_manager.categories[cat_name]["color"]
                else:
                    cat_folder_name = "Other"
                    cat_color = "#94A3B8"
                
                dest_dir = folder / cat_folder_name
                dest_dir.mkdir(parents=True, exist_ok=True)

                dest_file = dest_dir / file_path.name
                if dest_file.exists():
                    dest_file = self._get_unique_path(dest_dir, file_path.stem, file_path.suffix)

                shutil.move(str(file_path), str(dest_file))
                moved += 1
                self.log_callback(f"  ✓  {file_path.name}  →  {cat_folder_name}", cat_color)

            except Exception as e:
                errors += 1
                self.log_callback(f"  ✗  {file_path.name}: {e}", "#EF4444")

            progress_val = (i + 1) / total
            self.progress_callback(progress_val)
            time.sleep(0.03)

        self.log_callback(f"\n{'─'*40}", "#1E293B")
        self.log_callback(f"Done! Moved: {moved}  |  Errors: {errors}", "#34D399")
        
        return moved, errors

    def sort_by_date(self, folder_path):
        """
        Сортирует файлы по дате изменения (формат: YYYY-MM)
        
        Args:
            folder_path: путь к папке для сортировки
            
        Returns:
            Кортеж (количество перемещённых, количество ошибок)
        """
        folder = Path(folder_path)
        files = [f for f in folder.iterdir() if f.is_file()]
        
        # Сортируем по дате (новые первыми)
        files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

        if not files:
            self.log_callback("No files found!", "#EF4444")
            return 0, 0

        moved = 0
        errors = 0
        total = len(files)

        self.log_callback(f"\n{'─'*40}", "#1E293B")
        self.log_callback(f"Starting sorting {total} files (By Date)...", "#FBBF24")

        for i, file_path in enumerate(files):
            try:
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                cat_folder_name = mtime.strftime("%Y-%m")
                cat_color = "#A78BFA"
                dest_dir = folder / "By Date" / cat_folder_name
                
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / file_path.name
                if dest_file.exists():
                    dest_file = self._get_unique_path(dest_dir, file_path.stem, file_path.suffix)

                shutil.move(str(file_path), str(dest_file))
                moved += 1
                self.log_callback(f"  ✓  {file_path.name}  →  {cat_folder_name}", cat_color)

            except Exception as e:
                errors += 1
                self.log_callback(f"  ✗  {file_path.name}: {e}", "#EF4444")

            progress_val = (i + 1) / total
            self.progress_callback(progress_val)
            time.sleep(0.03)

        self.log_callback(f"\n{'─'*40}", "#1E293B")
        self.log_callback(f"Done! Moved: {moved}  |  Errors: {errors}", "#34D399")
        
        return moved, errors

    def sort_by_size(self, folder_path):
        """
        Сортирует файлы по размеру (Small, Medium, Large)
        
        Args:
            folder_path: путь к папке для сортировки
            
        Returns:
            Кортеж (количество перемещённых, количество ошибок)
        """
        folder = Path(folder_path)
        files = [f for f in folder.iterdir() if f.is_file()]
        
        # Сортируем по размеру (крупные первыми)
        files.sort(key=lambda f: f.stat().st_size, reverse=True)

        if not files:
            self.log_callback("No files found!", "#EF4444")
            return 0, 0

        moved = 0
        errors = 0
        total = len(files)

        self.log_callback(f"\n{'─'*40}", "#1E293B")
        self.log_callback(f"Starting sorting {total} files (By Size)...", "#FBBF24")

        for i, file_path in enumerate(files):
            try:
                size = file_path.stat().st_size
                if size < 1024 * 1024:
                    cat_folder_name = "Small (<1MB)"
                    cat_color = "#34D399"
                elif size < 100 * 1024 * 1024:
                    cat_folder_name = "Medium (1-100MB)"
                    cat_color = "#FBBF24"
                else:
                    cat_folder_name = "Large (>100MB)"
                    cat_color = "#EF4444"
                
                dest_dir = folder / "By Size" / cat_folder_name
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / file_path.name
                if dest_file.exists():
                    dest_file = self._get_unique_path(dest_dir, file_path.stem, file_path.suffix)

                shutil.move(str(file_path), str(dest_file))
                moved += 1
                self.log_callback(f"  ✓  {file_path.name}  →  {cat_folder_name}", cat_color)

            except Exception as e:
                errors += 1
                self.log_callback(f"  ✗  {file_path.name}: {e}", "#EF4444")

            progress_val = (i + 1) / total
            self.progress_callback(progress_val)
            time.sleep(0.03)

        self.log_callback(f"\n{'─'*40}", "#1E293B")
        self.log_callback(f"Done! Moved: {moved}  |  Errors: {errors}", "#34D399")
        
        return moved, errors

    @staticmethod
    def _get_unique_path(dest_dir, stem, suffix):
        """
        Генерирует уникальное имя файла, если файл уже существует
        
        Args:
            dest_dir: папка назначения
            stem: основная часть имени файла
            suffix: расширение файла
            
        Returns:
            Уникальный Path объект
        """
        dest_file = dest_dir / f"{stem}{suffix}"
        counter = 1
        while dest_file.exists():
            dest_file = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        return dest_file
