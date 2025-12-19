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
    stopwords = ('в', "—", "и","на", "с", "(", ")", "-")
    for wordy in stopwords:
        for l in words:
            if wordy == l:
                words.remove(wordy)
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
        dict: Словарь с метриками лексической плотности
    """
    try:
        import pymorphy3
        import re
        import sys
        
        # Проверяем, что текст - строка
        if not isinstance(text, str) or not text.strip():
            return {
                'lexical_density': 0.0,
                'noun_density': 0.0,
                'adj_density': 0.0,
                'verb_density': 0.0
            }
        
        # Инициализация анализатора с русским языком
        try:
            morph = pymorphy3.MorphAnalyzer(lang='ru')
        except:
            morph = pymorphy3.MorphAnalyzer()
        
        def preprocess_text(text):
            """Очистка текста для морфологического анализа"""
            # Приводим к нижнему регистру
            text = text.lower()
            # Оставляем только русские буквы и пробелы
            text = re.sub(r'[^а-яё\s]', ' ', text)
            # Убираем лишние пробелы
            text = re.sub(r'\s+', ' ', text).strip()
            return text
        
        def get_pos_tag(word):
            """Определяет часть речи для слова"""
            try:
                if len(word) < 2:  # Слишком короткие слова пропускаем
                    return 'OTHER'
                
                parsed = morph.parse(word)[0]
                pos = parsed.tag.POS
                
                # Существительные
                if pos in ['NOUN', 'NPRO']:
                    return 'NOUN'
                # Прилагательные
                elif pos in ['ADJF', 'ADJS', 'COMP']:
                    return 'ADJ'
                # Глаголы и их формы
                elif pos in ['VERB', 'INFN', 'GRND', 'PRTF', 'PRTS']:
                    return 'VERB'
                else:
                    return 'OTHER'
            except:
                return 'OTHER'
        
        # Обрабатываем текст
        processed_text = preprocess_text(text)
        words = [w for w in processed_text.split() if len(w) >= 2]  # Берем слова от 2 букв
        
        if not words:
            return {
                'lexical_density': 0.0,
                'noun_density': 0.0,
                'adj_density': 0.0,
                'verb_density': 0.0
            }
        
        # Считаем части речи
        counts = {'NOUN': 0, 'ADJ': 0, 'VERB': 0, 'OTHER': 0}
        for word in words:
            pos = get_pos_tag(word)
            counts[pos] += 1
        
        total = len(words)
        
        # Для отладки
        print(f"  Слов для анализа: {total}, существительных: {counts['NOUN']}, прилагательных: {counts['ADJ']}, глаголов: {counts['VERB']}")
        
        # Рассчитываем плотности
        noun_density = counts['NOUN'] / total if total > 0 else 0
        adj_density = counts['ADJ'] / total if total > 0 else 0
        verb_density = counts['VERB'] / total if total > 0 else 0
        lexical_density = (counts['NOUN'] + counts['ADJ'] + counts['VERB']) / total if total > 0 else 0
        
        return {
            'lexical_density': round(lexical_density, 4),
            'noun_density': round(noun_density, 4),
            'adj_density': round(adj_density, 4),
            'verb_density': round(verb_density, 4)
        }
        
    except ImportError:
        print("  pymorphy3 не установлен. Установите: pip install pymorphy3")
        return {
            'lexical_density': 0.0,
            'noun_density': 0.0,
            'adj_density': 0.0,
            'verb_density': 0.0
        }
    except Exception as e:
        print(f"  Ошибка при расчете лексической плотности: {e}")
        return {
            'lexical_density': 0.0,
            'noun_density': 0.0,
            'adj_density': 0.0,
            'verb_density': 0.0
        }
