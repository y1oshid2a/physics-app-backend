import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag import get_ai_answer

if __name__ == "__main__":
    title = "単振り子の周期について"
    content = "単振り子の周期はどのように求めますか？導出過程も教えてください。"
    
    print("質問:", title)
    print("内容:", content)
    print("\nAIの回答:")
    print("-" * 40)
    
    answer = get_ai_answer(title, content)
    print(answer)