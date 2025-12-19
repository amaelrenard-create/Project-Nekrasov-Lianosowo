import os

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

def read_csv_file(filepath):
    """
    Читает CSV файл и возвращает список словарей.

    Args:
        filepath (str): Путь к CSV файлу

    Returns:
        list: Список словарей, где ключи — названия колонок """

    data = []
    try:
        with open (filepath, "r", encoding = "utf-8") as file:
            content = file.readlines()
            headers = content[0].strip().split(',')
            for line in content[1:]:
                data_dict_for_one_row = {}
                values = line.strip().split(",")
                for i in range(len(values)):
                    data_dict_for_one_row[headers[i]] = values[i]
                data.append(data_dict_for_one_row)
        return data
    except FileNotFoundError:
        print (f"Файл не найден: {filepath}")
        return data
    except Exception as e:
        print (f'Ошибка при чтении файла {filepath}: {e}')
        return data

def write_csv_file(filepath, data, headers):
    """
    Записывает данные в CSV файл.

    Args:
        filepath (str): Полный путь к файлу, включая папку и название файла
                       Например: 'results/statistics.csv'
        data (list): Список списков [[val1, val2], [val1, val2], ...]
        headers (list): Список заголовков ['col1', 'col2']

    Returns:
        bool: True если успешно
    """
    import os
    folder = os.path.dirname(filepath)
    os.makedirs(folder, exist_ok=True)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(','.join(headers) + '\n')
            for row in data:
                f.write(','.join(str(v) for v in row) + '\n')
        if folder:
            l = True
    except Exception as e:
        print (f"Ошибка при записи файла {filepath}: {e}")   
    return l

def write_text_file(filepath, text):
    """
    Создаёт текстовый файл и записывает в него текст.

    Args:
        filepath (str): Путь и имя файла для записи
        text (str): Текст для записи

    Returns:
        bool: True, если запись прошла успешно, иначе False
    """
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(text)
        return True
    except Exception as e:
        print(f"Ошибка при записи файла {filepath}: {e}")
        return False

def get_files_in_folder(folder_path, extension='.txt'):
    
    """
    Получает список файлов в указанной папке с заданным расширением.

    Args:
        folder_path (str): Путь к папке
        extension (str): Расширение файлов (по умолчанию '.txt')

    Returns:
        list: Список имен файлов с указанным расширением
    """
    import os
    names = os.listdir(folder_path)
    list = []
    for filename in names: 
        if filename.endswith(extension):
            list.append(filename)
    return list

