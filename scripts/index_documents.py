import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag import load_and_index_document

if __name__ == "__main__":
    filepath = "data/mechanics.txt"
    count = load_and_index_document(filepath)
    print(f"{count}個のチャンクを登録しました")