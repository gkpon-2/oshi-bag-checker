"""
custom_items.py

このモジュールは「ユーザーが自由に追加した持ち物の整理」を担当する（新機能）。

入力欄に書かれた自由なテキスト（改行区切りやカンマ区切り）を、
1件ずつのきれいな持ち物リストに変換する。前後の空白を取り除き、空行や重複を除く。

UI（Streamlit / CLI）から入力の文字列を受け取り、checklist.py に渡せる形に整える橋渡し役。
"""


def parse_custom_items(raw_text):
    """
    入力されたテキストを、持ち物のリストに変換する関数。

    対応する区切り:
        - 改行（1行に1つ書くスタイル）
        - カンマ「,」「、」（1行にまとめて書くスタイル）

    処理内容:
        1. 改行とカンマで分割する
        2. それぞれの前後の空白を取り除く
        3. 空文字は捨てる
        4. 同じ持ち物が複数あれば最初の1つだけ残す

    引数:
        raw_text: 入力欄の文字列（None や空文字でも安全に動く）

    戻り値:
        きれいに整理された持ち物のリスト
    """
    # 入力が無い場合は空のリストを返す
    if not raw_text:
        return []

    # まず改行で分割する
    rough_lines = raw_text.replace("\r\n", "\n").split("\n")

    items = []
    for line in rough_lines:
        # 1行の中をカンマ（半角・全角）でさらに分割する
        parts = line.replace("、", ",").split(",")

        for part in parts:
            # 前後の空白を取り除く
            cleaned = part.strip()

            # 空文字でなく、まだ追加していないものだけリストに入れる
            if cleaned and cleaned not in items:
                items.append(cleaned)

    return items
