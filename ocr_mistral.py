import os
from mistralai import Mistral
from dotenv import load_dotenv
import argparse
from pathlib import Path

def extract_text_from_pdf(pdf_path, output_dir=None):
    """
    PDFからテキストを抽出してファイルに保存する関数
    
    Args:
        pdf_path (str): 処理するPDFファイルのパス
        output_dir (str, optional): 出力先ディレクトリ。指定がない場合はPDFと同じディレクトリに保存
    
    Returns:
        str: 保存先のパス
    """
    # .envファイルから環境変数を読み込む
    load_dotenv()
    
    # APIキーの取得
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError("MISTRAL_API_KEYが環境変数または.envファイルに設定されていません")
    
    # PDFファイルパスの処理
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")
    
    # 出力先の設定
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = pdf_path.parent
    
    output_file = output_dir / f"{pdf_path.stem}.txt"
    
    # Mistral APIクライアントの作成
    client = Mistral(api_key=api_key)
    
    print(f"PDFファイル '{pdf_path}' の処理を開始します...")
    
    # PDFをMistralにアップロード
    print("PDFをアップロード中...")
    uploaded_pdf = client.files.upload(
        file={
            "file_name": pdf_path.name,
            "content": open(pdf_path, "rb"),
        },
        purpose="ocr"
    )
    
    # アップロードしたPDFのサイン付きURLを取得
    signed_url = client.files.get_signed_url(file_id=uploaded_pdf.id)
    
    # OCR処理を実行
    print("OCR処理を実行中...")
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": signed_url.url,
        }
    )
    
    # 全ページのテキストを抽出して保存
    all_text = ""
    total_pages = len(ocr_response.pages)
    
    print(f"合計 {total_pages} ページのテキストを抽出します...")
    
    for i, page in enumerate(ocr_response.pages, 1):
        page_text = page.markdown or page.text or ""
        if page_text:
            all_text += f"--- ページ {i}/{total_pages} ---\n\n{page_text}\n\n"
    
    # 抽出されたテキストを保存
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_text)
    
    print(f"OCR結果を {output_file} に保存しました。")
    return str(output_file)

if __name__ == "__main__":
    # コマンドライン引数の処理
    parser = argparse.ArgumentParser(description="MistralAI OCRを使用してPDFからテキストを抽出します")
    parser.add_argument("pdf_path", help="処理するPDFファイルのパス")
    parser.add_argument("--output_dir", "-o", help="テキストの出力先ディレクトリ")
    args = parser.parse_args()
    
    try:
        extract_text_from_pdf(args.pdf_path, args.output_dir)
    except Exception as e:
        print(f"エラーが発生しました: {e}")