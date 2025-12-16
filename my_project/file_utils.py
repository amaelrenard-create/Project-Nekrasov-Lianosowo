import os

def read_text_file(filepath):
    pass


def read_csv_file(filepath):
    """
    Читает CSV файл и возвращает список словарей.

    Args:
        filepath (str): Путь к CSV файлу

    Returns:
        list: Список словарей, где ключи — названия колонок """

def read_csv_file(filepath):
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
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(",".join(str(v) for v in row) + "/n")
    if folder:
        l = True
    return l



def write_text_file(filepath, content):
    pass


def get_files_in_folder(folder_path, extension='.txt'):
    passdef get_files_in_folder(folder_path, extension='.txt'):
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



if __name__ == "__main__":
    files = get_files_in_folder('corpus', '.txt')
    print(f"Найдено файлов: {len(files)}")


def read_csv_file(filepath):
    """
    Читает CSV файл и возвращает список словарей.

    Args:
        filepath (str): Путь к CSV файлу

    Returns:
        list: Список словарей, где ключи — названия колонок """

def read_csv_file(filepath):
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

if __name__ == "__main__":
    metadata = read_csv_file('data/metadata.csv')

    print(f"Загружено записей: {len(metadata)}")

    if metadata:
        print("\nПервая запись:")
        print(metadata[0])

        print("\nВсе записи:")
        for row in metadata:
            print(f"  - {row['filename']}: {row['title']} ({row['author']}, {row['year']})")


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
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(",".join(str(v) for v in row) + "/n")
    if folder:
        l = True
    return l

if __name__ == "__main__":
    data = [["text1.txt","Ночью/Ничего нет","Всеволод Некрасов",None], ["text2.txt","быстро","Всеволод Некрасов",None]]
    headers = ["filename","title","author","year"]
    exmpl = write_csv_file("results/statistics.csv", data, headers)
    print(exmpl)
