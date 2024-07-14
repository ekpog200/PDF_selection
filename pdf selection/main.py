from trainsform_input_pdf import find_annots
from highlighting_text import *

def main():
    dict = find_annots()
    print(dict)
    highlighting_text(dict)


if __name__ == "__main__":
    main()

