"""
    kindle-translator
"""
import os
from os import path
from constant import TESSERACT_PATH, OUTPUT_TXT_FOLDER
from PIL import Image
import pytesseract

class OCR:
    """
    画像から文字起こしをするクラス
    """
    def extract_characters(
        self,
        page_number: int,
        file_name: str,
        img_file_path: str,
        lang: str = "eng"
    ) -> str:
    
        """
        :関数名:
            - extract_characters
        :機能:
            - 画像から文字を抽出する

        :引数:
            - page_number: 電子書籍全体のページ数(int型)
            - file_name: 保存したいファイルの名前兼フォルダの名前(str型)
            - img_file_path: 画像の保存先ファイルパス(str型)
        :戻り値:
            - 保存するテキストファイルの名前(str型)
        """
        print('画像からテキストへの変換を行います')
        # tesseractのパスを設定
        pytesseract.pytesseract.tesseract_cmd = path.join(TESSERACT_PATH, 'tesseract.exe')

        file_name_txt = f'{file_name}.txt'

        # テキストファイルを出力するファイルパスを指定
        txt_file_path = path.join(OUTPUT_TXT_FOLDER, file_name)
        os.mkdir(txt_file_path)
        os.chdir(txt_file_path)
        print(f'{txt_file_path}にテキストファイルを保存します')

        # picture_0.pngのような名前の画像を一枚ずつ読み込みして文字を抽出
        text_list = []
        for page in range(page_number):
            print(page)
            img = Image.open(f'{img_file_path}/picture_{page}.png')
            text = pytesseract.image_to_string(img, lang=lang)
            text += '\n' # 改行を追加
            text_list.append(text)

        # ひとつのテキストファイルに書き込み
        with open(file_name_txt, 'w', encoding='utf-8') as f:
            f.writelines(text_list)

        print('テキストファイルへの書き込みが終了しました')

        return file_name_txt, txt_file_path

    def divide_file(
        self,
        file_name: str,
        file_name_txt: str
    ) -> list:
        """
        :関数名:
            - divide_file
        :機能:
            - テキストファイルをDeepL APIにPOSTできる適度な大きさに分割(およそ100kbごと)

        :引数:
            - file_name: 保存したいファイルの名前兼フォルダの名前(str型)
            - file_name_txt: 保存したいテキストファイルの名前(str型)
        :戻り値:
            - file_list: 分割した複数のテキストファイルの名前(list型)
        """
        # read_data_size = 0
        num = 0
        file_list = []

        print('テキストファイルを分割します')

        # 対象ファイルを開いて10万字ごと(およそ100kbごと)に分割して保存
        f = open(file_name_txt, "r", encoding="utf-8")
        file = f.read()
        file_length = len(file)