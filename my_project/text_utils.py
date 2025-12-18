

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
    
def count_unique_words(text):
    words = text.lower().split()
    return len(set(words))

def calculate_ttr(text):
    words = text.lower().split()
    
    if not words:
        return 0
    
    unique_words = set(words)
    return len(unique_words) / len(words)

def get_most_common_words(text, n=10):
    words = text.lower().split()
    result = {}
    
    for word in words:
        result[word] = result.get(word, 0) + 1
    
    return sorted(result.items(), key=lambda x: x[1], reverse=True)[:n]

def count_lines(text):
    return len(text.splitlines())

def average_word_length(text):
    words = text.split()
    
    if not words:
        return 0
    
    total_length = sum(len(word) for word in words)
    return total_length / len(words)



