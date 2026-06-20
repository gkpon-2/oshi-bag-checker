"""
output.py

このモジュールは「チェックリストをテキストに整形して出力・保存する処理」を担当する。
画面表示やダウンロード用の文字列を作る部分と、CLI版でファイルに保存する部分をまとめている。

自由追加した持ち物も、この整形処理を通すことで txt ダウンロードに必ず含まれるようにしている。
"""

from datetime import datetime
from pathlib import Path

from oshi_bag.data import (
    EVENT_LABELS,
    WEATHER_LABELS,
    TEMPERATURE_LABELS,
    MEMO_ITEMS,
)


def create_output_text(
    event_type,
    weather_type,
    temperature_type,
    is_travel,
    checklist,
):
    """
    画面表示・保存用のテキストを作る関数。

    チェックリスト（持ち物）は create_checklist が作った最終結果をそのまま受け取るので、
    自由追加した持ち物もここに含まれた状態で渡ってくる。
    つまり、このテキストをダウンロードすれば自由追加分も一緒に保存される。
    """
    # 作成日（今日の日付）を文字列にする
    today = datetime.now().strftime("%Y-%m-%d")

    # 遠征の有無を日本語にする
    travel_text = "あり" if is_travel else "なし"

    # テキストを1行ずつ組み立てる（条件の見出し部分）
    lines = [
        "推し活現場もちものチェックリスト",
        f"作成日：{today}",
        "",
        "【条件】",
        f"現場タイプ：{EVENT_LABELS[event_type]}",
        f"天気：{WEATHER_LABELS[weather_type]}",
        f"気温：{TEMPERATURE_LABELS[temperature_type]}",
        f"遠征：{travel_text}",
        "",
        "【持ち物】",
    ]

    # 持ち物を1つずつ「□ 持ち物名」の形で追加する
    for item in checklist:
        lines.append(f"□ {item}")

    # 末尾のメモ項目を追加する
    lines.append("")
    lines.append("【メモ】")
    for memo in MEMO_ITEMS:
        lines.append(f"□ {memo}")

    # 行のリストを改行でつないで1つの文字列にして返す
    return "\n".join(lines)


def save_output(text):
    """
    作成したチェックリストを output フォルダに保存する関数（CLI版で使用）。

    output フォルダが無ければ作り、作成日時を入れたファイル名で保存する。
    """
    # 保存先フォルダ（無ければ作成する）
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # ファイル名に使う日時（例：20260501_115050）
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"checklist_{now}.txt"

    # テキストをUTF-8で書き込む
    file_path.write_text(text, encoding="utf-8")

    return file_path
