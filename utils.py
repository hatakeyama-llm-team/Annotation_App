# utils.py
class Constants:
    GOOD = "文章が成立している😁"
    PENDING = "部分的に文章が成立している🙄"
    BAD = "文章が成立していない😇"
    GOOD_POINT = 100
    PENDING_POINT = 50
    BAD_POINT = 0
    INSTRUCTIONS = """
    # 評価の流れ
    
    Q.1. テキストを読み込む

        1. テキストを読み込む
                    
        2. 読んだ文章を評価する
                    
        3. 文章が成立している/判断に困る/
           文章が成立していないのいずれかを選択する
                    
        4. 次の文章を読み込む
    
    Q.2. テキストを修正する
    
        1. テキストを読み込む
    
        2. 読んだ文章を修正する
    
        3. 修正した文章を保存する
        
        4. 次の文章を評価するをクリック（２回クリックお願いします）
                
                   """

    SHORTCUTS = f"""
        # Q1回答で便利なショートカットキー
        ```
        
        - {GOOD}   : Shift+A
        - {PENDING}: Shift+S
        - {BAD}    : Shift+D
         
         ```
        """

    MAIN_PAGE = 0
    LOGIN_PAGE = 1
    REGISTER_PAGE = 2
    MANAGEMENT_PAGE = 3
    ANNOTATION_PAGE = 4
