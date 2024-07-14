from trainsform_input_pdf import find_annots
from highlighting_text import *


def main() -> None:
    input_path = '../input_documents/'  # путь до файлов, где есть выделение
    processed_path = '../processed_documents/'  # путь до файлов, которые надо обработать
    output_path = '../output_documents/'  # путь до обработанных файлы (result)

    print("Обработка input файлов")
    dict_highlighting = find_annots(input_path)
    print("Обработка input файлов завершена")

    print("Обработка processed файлов")
    highlighting_text(dict_highlighting, processed_path, output_path)
    print("Обработка processed файлов завершена")


if __name__ == "__main__":
    main()

