def read_text_file(filepath):
    """
    Читает содержимое текстового файла.

    Args:
        filepath (str): Путь к файлу

    Returns:
        str: Содержимое файла или сообщение об ошибке
    """
    # Ваш код здесь
    try:
        with open(filepath,"r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return "Ошибка: Файл не найден"
    return content

def count_words(text):
    """
    Подсчитывает количество слов в тексте.

    Args:
        text (str): Текст для анализа

    Returns:
        int: Количество слов
    """
    text = text.split()
    count = len(text)
    return count

if __name__ == "__main__":
    text = read_text_file("corpus/text1.txt")
    print(count_words(text))