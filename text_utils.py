import os
from file_utils import read_text_file
def count_words(text):
    """
    Подсчитывает количество слов в тексте.

    Args:
        text (str): Текст для анализа

    Returns:
        int: Количество слов
    """
    for a in ",.-—;:'?!":
        if a in text:
            text = text.replace(a, "")
    text = text.strip().split()
    count = len(text)
    return count          


if __name__ == "__main__":
    text = read_text_file("corpus/text1.txt")
    print(count_words(text))