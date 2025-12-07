import os
from file_utils import get_files_in_folder, read_text_file

def main():
    """Главная функция программы."""
    print("=" * 60)
    print("📂 Анализ текстовых файлов в корпусе")
    print("=" * 60)

    # 1. Получить список файлов
    corpus_folder = 'corpus'
    print(f"\n🔍 Поиск файлов в папке '{corpus_folder}'...")
    files = get_files_in_folder(corpus_folder, ".txt")

    if not files:
        print("❌ Файлы не найдены!")
        return

    print(f"✅ Найдено файлов: {len(files)}")
    print("\nСписок файлов:")
    for file in files:
        print(f"-{file}")

    # 2. Прочитать и показать содержимое каждого файла
    print(f"\n{'=' * 60}")
    print("📄 Содержимое файлов:")
    print("=" * 60)

    for filename in files:
        filepath = os.path.join("corpus", filename)
        print(f"\nЧтение файла: {filename}")
        print("=" * 50)
        content = read_text_file(filepath)
        print(content)
        print("=" * 50)



