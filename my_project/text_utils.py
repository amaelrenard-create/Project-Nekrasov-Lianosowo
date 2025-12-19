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


def calculate_lexical_density(text):
    """
    Вычисляет лексическую плотность для ВСЕГО текста.
    
    Args:
        text (str): Исходный текст
    
    Returns:
        dict: Словарь с метриками лексической плотности:
            - 'lexical_density': общая лексическая плотность (доля)
            - 'noun_density': плотность существительных (доля)
            - 'adj_density': плотность прилагательных (доля)
            - 'verb_density': плотность глаголов (доля)
    """
    try:
        import pymorphy3
        import re
    except ImportError:
        print("Внимание: Для расчета лексической плотности установите pymorphy3: pip install pymorphy3")
        return {
            'lexical_density': 0.0,
            'noun_density': 0.0,
            'adj_density': 0.0,
            'verb_density': 0.0
        }
    
    # Инициализация анализатора
    morph = pymorphy3.MorphAnalyzer()
    
    def preprocess_text(text):
        """Очистка текста для морфологического анализа"""
        if not isinstance(text, str):
            return ""
        text = re.sub(r'[^\w\s]', ' ', text)
        text = text.lower()
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def get_pos_tag(word):
        """Определяет часть речи для слова"""
        try:
            parsed = morph.parse(word)[0]
            pos = parsed.tag.POS
            if pos in ['NOUN', 'NPRO']:
                return 'NOUN'
            elif pos in ['ADJF', 'ADJS', 'COMP']:
                return 'ADJ'
            elif pos in ['VERB', 'INFN', 'GRND', 'PRTF', 'PRTS']:
                return 'VERB'
            else:
                return 'OTHER'
        except:
            return 'OTHER'
    
    # Основная логика
    processed_text = preprocess_text(text)
    words = processed_text.split()
    total_words = len(words)
    
    if total_words == 0:
        return {
            'lexical_density': 0.0,
            'noun_density': 0.0,
            'adj_density': 0.0,
            'verb_density': 0.0
        }
    
    # Считаем части речи
    pos_counts = {'NOUN': 0, 'ADJ': 0, 'VERB': 0, 'OTHER': 0}
    for word in words:
        pos = get_pos_tag(word)
        if pos in pos_counts:
            pos_counts[pos] += 1
    
    # Вычисляем плотности
    noun_density = pos_counts['NOUN'] / total_words
    adj_density = pos_counts['ADJ'] / total_words
    verb_density = pos_counts['VERB'] / total_words
    lexical_density = (pos_counts['NOUN'] + pos_counts['ADJ'] + pos_counts['VERB']) / total_words
    
    return {
        'lexical_density': round(lexical_density, 4),
        'noun_density': round(noun_density, 4),
        'adj_density': round(adj_density, 4),
        'verb_density': round(verb_density, 4)
    }
