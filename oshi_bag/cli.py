"""
cli.py

このモジュールは「コマンドライン版（CLI）の対話処理」を担当する。
ターミナル上でユーザーに質問し、選んだ条件をもとにチェックリストを作って表示・保存する。

画面まわりの処理（入力を受け取る・表示する）だけをここに置き、
チェックリストの中身を作る計算は checklist.py / output.py に任せている。
"""

from oshi_bag.data import (
    EVENT_LABELS,
    WEATHER_LABELS,
    TEMPERATURE_LABELS,
)
from oshi_bag.checklist import create_checklist
from oshi_bag.output import create_output_text, save_output
from oshi_bag.custom_items import parse_custom_items


def select_option(title, options):
    """
    選択肢を表示して、ユーザーに1つ選んでもらう関数。

    番号付きで選択肢を表示し、正しい番号が入力されるまで聞き直す。
    戻り値は選ばれた選択肢のキー（live / sunny など）。
    """
    print()
    print(title)

    # 選択肢のキー一覧（例：["live", "stage", "meet", "online"]）
    keys = list(options.keys())

    # 1から始まる番号付きで選択肢を表示する
    for index, key in enumerate(keys, start=1):
        print(f"{index}. {options[key]}")

    # 正しい番号が来るまで繰り返し聞く
    while True:
        choice = input("番号を入力してください >> ")

        # 数字かどうかを確認する
        if choice.isdigit():
            choice_number = int(choice)

            # 選択肢の範囲内なら、その番号に対応するキーを返す
            if 1 <= choice_number <= len(keys):
                return keys[choice_number - 1]

        print("正しい番号を入力してください。")


def ask_yes_no(message):
    """
    y / n で答えてもらう関数。

    正しく y か n が入力されるまで聞き直し、True / False を返す。
    """
    while True:
        answer = input(f"{message} (y/n) >> ").lower()

        if answer == "y":
            return True

        if answer == "n":
            return False

        print("y または n で入力してください。")


def ask_custom_items():
    """
    自由に追加したい持ち物を入力してもらう関数（新機能のCLI版）。

    カンマ区切りで入力してもらい、parse_custom_items できれいなリストに変換する。
    何も入力しなければ追加なし（空のリスト）。
    """
    print()
    print("自由に追加したい持ち物があれば入力してください（カンマ区切り / 無ければそのままEnter）")
    raw_text = input("追加の持ち物 >> ")

    return parse_custom_items(raw_text)


def run_cli():
    """
    CLIアプリ全体の流れをまとめる関数。

    質問 → チェックリスト作成 → 表示 → 保存の有無を確認、という一連の流れを実行する。
    """
    print("================================")
    print("推し活現場もちものチェックリスト")
    print("================================")

    # 1. 現場タイプを選んでもらう
    event_type = select_option(
        "現場タイプを選んでください",
        EVENT_LABELS,
    )

    # 2. 天気を選んでもらう
    weather_type = select_option(
        "天気を選んでください",
        WEATHER_LABELS,
    )

    # 3. 気温を選んでもらう
    temperature_type = select_option(
        "気温を選んでください",
        TEMPERATURE_LABELS,
    )

    # 4. 遠征かどうかを聞く
    is_travel = ask_yes_no("遠征ですか？")

    # 5. 自由追加の持ち物を聞く（新機能）
    custom_items = ask_custom_items()

    # 6. 条件と自由追加分をまとめてチェックリストを作る
    checklist = create_checklist(
        event_type,
        weather_type,
        temperature_type,
        is_travel,
        custom_items,
    )

    # 7. 保存・表示用のテキストを作る（自由追加分もここに含まれる）
    output_text = create_output_text(
        event_type,
        weather_type,
        temperature_type,
        is_travel,
        checklist,
    )

    # 8. 画面に表示する
    print()
    print(output_text)

    # 9. 保存するか聞いて、必要なら output フォルダに保存する
    should_save = ask_yes_no("このチェックリストを保存しますか？")

    if should_save:
        file_path = save_output(output_text)
        print()
        print(f"保存しました：{file_path}")
    else:
        print()
        print("保存せずに終了しました。")
