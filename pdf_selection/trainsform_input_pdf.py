import os
import pymupdf as fitz
from itertools import groupby


def find_hightlight_text(page, rect) -> tuple[str, str]:
    """
    Функция нахождения текста под выделенной области rect

    :param page: (fitz.page) обрабатываемая страница
    :param rect: (fitz.Rect) координаты x0, y0, y1, y2 выделенного прямоугольника в pdf
    :return key, value для словаря
    """
    # список слов в tuple на странице
    words = page.get_text("words")
    # ищем по координатам текста (w[:4]) выделенной аннотацией области (rect)
    words.sort(key=lambda w: (w[3], w[0]))
    mywordvalues = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
    # для нахождения значений в 1м столбце, берём всю ширину листа (x0, x1) и высоту от rect (y0, y1)
    mywordskeys = [w for w in words if fitz.Rect(w[:4]).intersects(fitz.Rect(5, rect[1], page.rect.width, rect[3]))]

    groupvalues = groupby(mywordvalues, key=lambda w: w[3])
    group = groupby(mywordskeys, key=lambda w: w[3])

    result = []  # массив слов keys [[]]
    # соединяем полученные отдельные слова (под созданным нами rect) в текст для key
    for y1, gwords in group:
        # print(" ".join(w[4] for w in gwords))
        result.append(" ".join(w[4] for w in gwords).split())

    # соединяем полученные отдельные слова (под созданным нами rect) в текст для value
    resultvalues = []  # массив слов values [[]]
    for y1, gwords in groupvalues:
        # print(" ".join(w[4] for w in gwords))
        resultvalues.append(" ".join(w[4] for w in gwords).split())

    result2 = []
    # из массива переходим в список и убираем из него значения values
    for row in result:
        for value in row[:]:
            if value not in resultvalues[0]:
                result2.append(value)

    result2 = " ".join(result2)
    resultvalues = " ".join(resultvalues[0])
    return result2, resultvalues


def find_annots(input_path: str) -> dict:
    """
    Функция нахождения аннотаций (выделенный текст) на странице

    :param input_path: путь до обрабатываемых файлов
    :return: возвращает словарь с выделенным текстом
    """
    # смотрим все файлы в input_documents (с заранее закрашенными полями) и обрабатываем их
    all_input_files = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]
    all_input_files.remove('.gitkeep')
    if len(all_input_files) == 0:
        raise FileNotFoundError("Поместите хотя бы один файл для обработки")
    # словарь для хранения всех выделенных слов в input файлах
    result_dict = {}
    for file in all_input_files:
        doc = fitz.open(os.path.join(input_path, file))
        # Итерируемся по всем страницам в каждом файле
        for page in doc:
            # смотрим все аннотации на странице
            annots = page.annots()
            # Итерируемся по аннотациям на странице
            for annot in annots:
                # Проверяем, является ли аннотация выделением текста
                if annot.type[0] == 8:
                    # добавляем в словарь result_dict выделенный текст
                    k, v = find_hightlight_text(page, annot.rect)
                    if k not in result_dict:
                        result_dict[k] = v
        doc.close()
    return result_dict


