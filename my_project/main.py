import os
from file_utils import get_files_in_folder, read_text_file, read_csv_file, write_csv_file
from text_utils import count_words

def main():
    """Главная функция программы."""
    print("=" * 60)
    print("📂 Анализ текстовых файлов в корпусе")
    print("=" * 60)

    # 1. Получить список файлов
    corpus_folder = 'corpus'
    print(f"\n🔍 Поиск файлов в папке '{corpus_folder}'...")
    files = get_files_in_folder(corpus_folder, '.txt')

    if not files:
        print("❌ Файлы не найдены!")
        return

    print(f"✅ Найдено файлов: {len(files)}")
    print("\nСписок файлов:")
    # your code here
    for file in files:
        print(f"-{file}")

    # 2. Прочитать и показать содержимое каждого файла
    print(f"\n{'=' * 60}")
    print("📄 Содержимое файлов:")
    print("=" * 60)

    for filename in files:
        filepath = os.path.join('corpus', filename)
        print(f"\nЧтение файла: {filename}")
        print("-" * 50)
        content = read_text_file(filepath)
        print(content)
        print("-" * 50)

    print("\n✅ Обработка завершена!")
    pass

def analyze_corpus(corpus_folder):
    """
    Анализирует все тексты в папке, сохраняет результаты и выводит статистику.

    Args:
        corpus_folder (str): Путь к папке с текстами (например, 'corpus')
    """
    print("=" * 60)
    print("📊 Анализ корпуса текстов")
    print("=" * 60)
    files = get_files_in_folder(corpus_folder, '.txt')

    if not files:
        print("❌ Файлы не найдены!")
        return
    data = []
    for file in files:
        list_inf = []
        list_inf.append(f"{file}")
        text = read_text_file(f"{corpus_folder}/{file}")
        wordnum = count_words(text)
        list_inf.append(wordnum)
        data.append(list_inf)
    head = ['filename', 'word_count']
    write_csv_file("results/statistics.csv", data, head)
    results_list = read_csv_file("results/statistics.csv")
    print(f"✅ Проанализировано файлов: {len(files)}")
    print(f"Результаты сохранены в results/statistics.csv\n")
    sum = 0
    i = 0
    for nam in results_list:
        print (f"{nam["filename"]}: {nam["word_count"]} слов")
        sum += int(nam["word_count"])
        i += 1
    print ("Общее количество слов в корпусе:", sum)
    mid = sum/i
    print ("Среднее число слов:", round(mid, 2))

if __name__ == '__main__':
    analyze_corpus("corpus")
