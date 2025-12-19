import os
from file_utils import read_text_file

def count_words(text):
    """
    Подсчитывает количество слов в тексте

    Args:
        text (str): Текст для анализа

    Returns:
        int: Количество слов
    """
    text = text.split()
    count = len(text)
    return count
    
def count_unique_words(text):
    """
    Подсчитывает количество уникальных слов в тексте

    Args:
        text (str): Входной текст

    Returns:
        int: Количество уникальных слов
    """
    words = text.lower().split()
    return len(set(words))

def calculate_ttr(text):
    """
    Вычисляет TTR = количество уникальных слов / общее количество слов

    Args:
        text (str): Входной текст

    Returns:
        float: TTR текста (от 0 до 1). Если слов нет, возвращает 0
    """
    words = text.lower().split()
    
    if not words:
        return 0
    
    unique_words = set(words)
    return len(unique_words) / len(words)

def get_most_common_words(text, n=10):
    """
    Находит n самых часто встречающихся слов

    Args:
        text (str): Входной текст.
        n (int): Количество самых частых слов для возврата (10)

    Returns:
        list of tuples: Список кортежей вида (слово, количество), 
                        отсортированных по убыванию частоты
    """
    words = text.lower().split()
    result = {}
    
    for word in words:
        result[word] = result.get(word, 0) + 1
    
    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:n]

def count_lines(text):
    """
    Подсчитывает количество строк в тексте.

    Args:
        text (str): Входной текст

    Returns:
        int: Количество строк (включая пустые)
    """
    return len(text.splitlines())

def average_word_length(text):
    """
    Вычисляет среднюю длину слова в тексте.

    Args:
        text (str): Входной текст.

    Returns:
        float: Средняя длина слова. Если слов нет, возвращает 0.
    """
    words = text.split()
    
    if not words:
        return 0
    
    total_length = sum(len(word) for word in words)
    return total_length / len(words)


if __name__ == "__main__":
    text = read_text_file("corpus/limonov001.txt")
    print(count_words(text))

