
import os
from file_utils import get_files_in_folder, read_text_file, read_csv_file, write_csv_file
from text_utils import count_words, count_unique_words, calculate_ttr, get_most_common_words, count_lines, average_word_length, calculate_lexical_density

def analyze_single_text(filepath, filename):
    """
    Анализирует один текстовый файл.
    
    Args:
        filepath (str): Полный путь к файлу
        filename (str): Имя файла
    
    Returns:
        dict: Словарь с результатами анализа или None в случае ошибки
    """
    # Чтение файла
    text = read_text_file(filepath)
    
    if text.startswith("Ошибка"):
        print(f"  ⚠️ Пропуск {filename}: {text}")
        return None
    
    # Базовые метрики
    result = {
        'filename': filename,
        'word_count': count_words(text),
        'unique_words': count_unique_words(text),
        'ttr': calculate_ttr(text),
        'line_count': count_lines(text),
        'avg_word_length': average_word_length(text),
    }
    
    # Лексическая плотность (если функция доступна)
    try:
        lex_metrics = calculate_lexical_density(text)
        result.update({
            'lexical_density': lex_metrics['lexical_density'],
            'noun_density': lex_metrics['noun_density'],
            'adj_density': lex_metrics['adj_density'],
            'verb_density': lex_metrics['verb_density'],
        })
    except NameError:
        # Если функция calculate_lexical_density не импортирована
        print(f"  ⚠️ Функция лексической плотности не доступна для {filename}")
    
    return result

def analyze_corpus(corpus_folder='corpus'):
    """
    Анализирует все тексты в папке, сохраняет результаты и выводит статистику.
    
    Args:
        corpus_folder (str): Путь к папке с текстами (например, 'corpus')
    
    Returns:
        list: Список словарей с результатами анализа
    """
    print("=" * 60)
    print("📊 Анализ корпуса текстов")
    print("=" * 60)
    
    # 1. Получаем список файлов
    files = get_files_in_folder(corpus_folder, '.txt')
    
    if not files:
        print("❌ Файлы не найдены!")
        return []
    
    print(f"✅ Найдено файлов: {len(files)}")
    
    # 2. Создаем папку results, если её нет
    if not os.path.exists('results'):
        os.makedirs('results')
        print("📁 Создана папка 'results/'")
    
    # 3. Анализируем каждый файл
    all_results = []
    
    print(f"\n🔍 Анализ файлов:")
    for i, filename in enumerate(files, 1):
        print(f"  {i}/{len(files)}: {filename}... ", end="")
        
        filepath = os.path.join(corpus_folder, filename)
        result = analyze_single_text(filepath, filename)
        
        if result:
            all_results.append(result)
            print("✅")
        else:
            print("❌")
    
    # 4. Загружаем метаданные (если есть)
    metadata = {}
    metadata_path = 'data/metadata.csv'
    
    if os.path.exists(metadata_path):
        print(f"\n📄 Загружаем метаданные из {metadata_path}...")
        metadata_list = read_csv_file(metadata_path)
        
        # Преобразуем в словарь для удобного доступа
        for item in metadata_list:
            if 'filename' in item:
                metadata[item['filename']] = item
        print(f"✅ Загружено {len(metadata)} записей")
    else:
        print(f"\n⚠️ Файл метаданных не найден: {metadata_path}")
        print("  Будут использованы только базовые метрики")
    
    # 5. Объединяем результаты с метаданными
    enriched_results = []
    for result in all_results:
        filename = result['filename']
        enriched_result = result.copy()
        
        if filename in metadata:
            # Добавляем метаданные
            enriched_result.update({
                'title': metadata[filename].get('title', 'Неизвестно'),
                'author': metadata[filename].get('author', 'Неизвестно'),
                'year': metadata[filename].get('year', 'Неизвестно'),
                'genre': metadata[filename].get('genre', 'Неизвестно'),
            })
        else:
            # Если метаданных нет, заполняем заглушками
            enriched_result.update({
                'title': 'Неизвестно',
                'author': 'Неизвестно',
                'year': 'Неизвестно',
                'genre': 'Неизвестно',
            })
        
        enriched_results.append(enriched_result)
    
    # 6. Сохраняем результаты в CSV
    print(f"\n💾 Сохранение результатов...")
    
    # Определяем заголовки для CSV
    headers = [
        'filename', 'title', 'author', 'year', 'genre',
        'word_count', 'unique_words', 'ttr', 'line_count',
        'avg_word_length', 'lexical_density', 'noun_density',
        'adj_density', 'verb_density'
    ]
    
    # Фильтруем заголовки, оставляем только те, что есть в данных
    available_headers = []
    for header in headers:
        if any(header in result for result in enriched_results):
            available_headers.append(header)
    
    # Готовим данные для записи (только доступные поля)
    csv_data = []
    for result in enriched_results:
        row = []
        for header in available_headers:
            row.append(result.get(header, ''))
        csv_data.append(row)

    write_csv_file("results/statistics.csv", csv_data, available_headers)
    print(f"✅ Результаты сохранены в results/statistics.csv")
    
    # 7. Генерируем и сохраняем текстовый отчет
    generate_report(enriched_results, corpus_folder)
    
    # 8. Выводим сводную статистику
    print_summary(enriched_results)
    
    return enriched_results

def generate_report(results, corpus_folder):
    """
    Генерирует текстовый отчет с результатами анализа.
    
    Args:
        results (list): Список словарей с результатами
        corpus_folder (str): Путь к папке корпуса
    """
    if not results:
        return
    
    report_lines = []
    
    # Заголовок отчета
    report_lines.append("=" * 60)
    report_lines.append("📊 ОТЧЕТ ПО АНАЛИЗУ ТЕКСТОВОГО КОРПУСА")
    report_lines.append("=" * 60)
    report_lines.append(f"Папка корпуса: {corpus_folder}")
    report_lines.append(f"Дата анализа: {os.path.basename(corpus_folder)}")
    report_lines.append("")
    
    # Общая статистика
    report_lines.append("📈 ОБЩАЯ СТАТИСТИКА:")
    report_lines.append("-" * 40)
    
    total_files = len(results)
    total_words = sum(r.get('word_count', 0) for r in results)
    total_unique = sum(r.get('unique_words', 0) for r in results)
    avg_ttr = sum(r.get('ttr', 0) for r in results) / total_files if total_files > 0 else 0
    
    report_lines.append(f"  Всего файлов: {total_files}")
    report_lines.append(f"  Всего слов: {total_words:,}")
    report_lines.append(f"  Всего уникальных слов: {total_unique:,}")
    report_lines.append(f"  Средний TTR: {avg_ttr:.4f}")
    
    # Статистика по лексической плотности (если есть)
    if any('lexical_density' in r for r in results):
        avg_lex = sum(r.get('lexical_density', 0) for r in results) / total_files
        report_lines.append(f"  Средняя лексическая плотность: {avg_lex:.2%}")
        report_lines.append("")
    
    # Детальная статистика по файлам
    report_lines.append("")
    report_lines.append("📋 ДЕТАЛЬНАЯ СТАТИСТИКА ПО ФАЙЛАМ:")
    report_lines.append("=" * 60)
    
    for i, result in enumerate(results, 1):
        report_lines.append(f"\n{i}. 📄 {result.get('filename', 'Неизвестно')}")
        report_lines.append("-" * 40)
        
        if 'title' in result:
            report_lines.append(f"   Название: {result.get('title', 'Неизвестно')}")
        if 'author' in result:
            report_lines.append(f"   Автор: {result.get('author', 'Неизвестно')}")
        if 'year' in result:
            report_lines.append(f"   Год: {result.get('year', 'Неизвестно')}")
        
        report_lines.append(f"   Слов: {result.get('word_count', 0):,}")
        report_lines.append(f"   Уникальных слов: {result.get('unique_words', 0):,}")
        report_lines.append(f"   TTR: {result.get('ttr', 0):.4f}")
        report_lines.append(f"   Строк: {result.get('line_count', 0):,}")
        report_lines.append(f"   Ср. длина слова: {result.get('avg_word_length', 0):.2f}")
        
        if 'lexical_density' in result:
            report_lines.append(f"   Лекс. плотность: {result.get('lexical_density', 0):.2%}")
    
    # Выводы
    report_lines.append("\n" + "=" * 60)
    report_lines.append("💡 ВЫВОДЫ И НАБЛЮДЕНИЯ:")
    report_lines.append("=" * 60)
    
    if results:
        # Самый большой файл
        biggest_file = max(results, key=lambda x: x.get('word_count', 0))
        report_lines.append(f"• Самый большой файл: {biggest_file.get('filename')} "
                          f"({biggest_file.get('word_count', 0):,} слов)")
        
        # Самый лексически разнообразный
        most_diverse = max(results, key=lambda x: x.get('ttr', 0))
        report_lines.append(f"• Самый лексически разнообразный: {most_diverse.get('filename')} "
                          f"(TTR: {most_diverse.get('ttr', 0):.4f})")
        
        # Самая высокая лексическая плотность
        if any('lexical_density' in r for r in results):
            most_dense = max(results, key=lambda x: x.get('lexical_density', 0))
            report_lines.append(f"• Наибольшая лексическая плотность: {most_dense.get('filename')} "
                              f"({most_dense.get('lexical_density', 0):.2%})")
        
        # По авторам (если есть информация)
        authors = {}
        for result in results:
            author = result.get('author', 'Неизвестно')
            if author not in authors:
                authors[author] = []
            authors[author].append(result)
        
        if len(authors) > 1:
            report_lines.append(f"\n• Всего авторов: {len(authors)}")
            for author, files in authors.items():
                report_lines.append(f"  - {author}: {len(files)} файлов")
    
    report_lines.append("\n" + "=" * 60)
    report_lines.append("✅ Анализ завершен успешно!")
    report_lines.append("=" * 60)
    
    # Сохраняем отчет в файл
    report_content = "\n".join(report_lines)
    write_csv_file("results/report.txt", [{'report': report_content}], ['report'])
    
    # Также сохраняем как обычный текстовый файл
    with open("results/report.txt", "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"✅ Отчет сохранен в results/report.txt")

def print_summary(results):
    """
    Выводит сводную статистику в консоль.
    
    Args:
        results (list): Список словарей с результатами
    """
    if not results:
        return
    
    print("\n" + "=" * 60)
    print("📊 СВОДНАЯ СТАТИСТИКА")
    print("=" * 60)
    
    total_files = len(results)
    total_words = sum(r.get('word_count', 0) for r in results)
    total_unique = sum(r.get('unique_words', 0) for r in results)
    
    print(f"📁 Всего проанализировано файлов: {total_files}")
    print(f"🔤 Общее количество слов в корпусе: {total_words:,}")
    print(f"✨ Уникальных слов: {total_unique:,}")
    
    if total_files > 0:
        avg_words = total_words / total_files
        print(f"📊 Среднее число слов в файле: {avg_words:,.2f}")
    
    # Если есть данные о лексической плотности
    if any('lexical_density' in r for r in results):
        total_lex = sum(r.get('lexical_density', 0) for r in results)
        avg_lex = total_lex / total_files if total_files > 0 else 0
        print(f"📈 Средняя лексическая плотность: {avg_lex:.2%}")

def main():
    """Главная функция программы."""
    print("=" * 60)
    print("📚 Анализ текстового корпуса")
    print("=" * 60)

    # Проверяем наличие папки corpus
    corpus_folder = 'corpus'
    if not os.path.exists(corpus_folder):
        print(f"❌ Папка '{corpus_folder}' не найдена!")
        print("   Убедитесь, что папка с текстами существует.")
        return

    # Запускаем анализ корпуса
    results = analyze_corpus(corpus_folder)

    if results:
        print("\n" + "=" * 60)
        print("🎉 Анализ успешно завершен!")
        print("=" * 60)
        print("📁 Результаты сохранены в папке 'results/'")
        print("   - statistics.csv: детальные метрики по файлам")
        print("   - report.txt: полный отчет с выводами")
    else:
        print("\n❌ Анализ не дал результатов. Проверьте файлы в корпусе.")

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()
