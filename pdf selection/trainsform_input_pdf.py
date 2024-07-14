import os
import pymupdf as fitz
from itertools import groupby


# def tip() ->dict[str:int]:
#     path = '../input_documents/РВЭ_г_Москва,_Holland_park,_Корпус_11_Закрашены_ячейки.pdf'
#     text = {}
#     with fitz.open(path) as doc:
#         for page in doc:
#             for block in page.get_text("words"):
#                 print(block)
#                 if block[0] == "Text":
#                     for line in block[1]:
#                         print(line)
#
# tip()

def find_hightlight_text(page, rect):
    """Return text containted in the given rectangular highlighted area.

    Args:
        page (fitz.page): the associated page.
        rect (fitz.Rect): rectangular highlighted area.
    """
    # 5, ann[1], page.rect.width, ann[3]
    words = page.get_text("words")  # list of words on page

    words.sort(key=lambda w: (w[3], w[0]))  # ascending y, then x
    mywordvalues = [w for w in words if fitz.Rect(w[:4]).intersects(rect)]
    mywordskeys = [w for w in words if fitz.Rect(w[:4]).intersects(fitz.Rect(5, rect[1], page.rect.width, rect[3]))]

    # print(mywordskeys)
    groupvalues = groupby(mywordvalues, key=lambda w: w[3])
    group = groupby(mywordskeys, key=lambda w: w[3])
    result = []
    for y1, gwords in group:
        # print(" ".join(w[4] for w in gwords))
        result.append(" ".join(w[4] for w in gwords).split())

    resultvalues = []
    for y1, gwords in groupvalues:
        # print(" ".join(w[4] for w in gwords))
        resultvalues.append(" ".join(w[4] for w in gwords).split())
    result2 = []
    for row in result:
        for value in row[:]:
            if value not in resultvalues[0]:
                result2.append(value)

    result2 = " ".join(result2)
    resultvalues = " ".join(resultvalues[0])
    return result2, resultvalues


def find_annots():
    path = '../input_documents/РВЭ_г_Москва,_Holland_park,_Корпус_11_Закрашены_ячейки.pdf'
    doc = fitz.open(path)
    result_dict = {}

    # Итерируемся по всем страницам
    for page in doc:
        annots = page.annots()
        # Итерируемся по аннотациям на странице
        for annot in annots:
            # Проверяем, является ли аннотация выделением текста
            if annot.type[0] == 8:
                k, v = find_hightlight_text(page, annot.rect)
                result_dict[k] = v
    return result_dict



# def main():
#     path = '../input_documents/РВЭ_г_Москва,_Holland_park,_Корпус_11_Закрашены_ячейки.pdf'
#     doc = fitz.open(path)
#     for page in doc:
#         tabs = page.find_tables()
#         if tabs.tables:
#             table = tabs[0]
#             table_data = table.extract()

            # for row in table_data:
            #     print(row)
            # for row in table_data:
            #     # Предполагаем, что таблица имеет 2 колонки
            #     if len(row) == 2:
            #         label, cell = row
            #         annot = page.get_annot_at(cell[0], cell[1])
            #         if annot:
            #             if annot.type[0] == 8:
            #                 print(f"Наименование: {label}")
            #                 print(f"Выделенный текст: {cell}")
            #             else:
            #                 print(f"Наименование: {label}")
            #                 print(f"Текст в ячейке: {cell}")
            #         else:
            #             print(f"Наименование: {label}")
            #             print(f"Текст в ячейке: {cell}")
            #     else:
            #         print(f"Неожиданное количество колонок в строке: {row}")
        # if tabs.tables:
        #     print(tabs[0].extract())

    # doc.close()

