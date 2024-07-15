import pymupdf as fitz
import os


def add_highlight(page, rect) -> None:
    """
    Выделение аннотацией текста.

    :param page: (fitz.page) рассматриваемая страница в текущий момент.
    :param rect: (fitz.page) рассматриваемая страница в текущий момент.
    """
    annot = page.add_highlight_annot(rect)
    annot.set_colors(stroke=(1, 0.77, 0.6))
    annot.update()


def highlighting_text(htext: dict, processed_path: str, output_path: str) -> None:
    """
    Функция нахождения обрабатываемых файлов и их выделение

    :param htext: словарь выделенных слов с input_documents
    :param processed_path: путь до обрабатываемых файлов
    :param output_path: путь до итоговых файлов

    """
    # Просмотр всех необходимых к доработке файлов в processed_path
    all_proccessed_files = [f for f in os.listdir(processed_path) if os.path.isfile(os.path.join(processed_path, f))]
    all_proccessed_files.remove('.gitkeep')
    if len(all_proccessed_files) == 0:
        raise FileNotFoundError("Поместите хотя бы один файл для обработки")

    # проходим по всем обрабатываемым файлам
    for file in all_proccessed_files:
        doc = fitz.open(os.path.join(processed_path, file))
        # проходим по каждой странице в доке
        for page in doc:
            tabs = page.find_tables()
            # проходим по каждой таблице на листе
            for tab in tabs:
                # проходим по каждой ячейке, находим совпадения с данными из input_documents и выделяем 2й столбец
                for i, line in enumerate(tab.extract()):
                    for k in htext.keys():
                        if k in line[0].replace('\n', ' '):
                            # print(line[0].replace('\n', ' '))
                            add_highlight(page, fitz.Rect(tab.rows[i].cells[1]))

                    # if line[0].replace('\n', ' ') in htext.keys():
                    #     add_highlight(page, fitz.Rect(tab.rows[i].cells[1]))
        doc.save(os.path.join(output_path, file))
        doc.close()
