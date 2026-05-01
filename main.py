from datetime import datetime
from pathlib import Path


# 基本の持ち物リスト
BASE_ITEMS = [
    "チケット",
    "スマホ",
    "財布",
    "身分証",
    "モバイルバッテリー",
    "アクスタ・トレカ",
    "ハンカチ",
    "ティッシュ",
    "常備薬",
]


# 現場タイプ別の持ち物リスト
EVENT_ITEMS = {
    "live": [
        "ペンライト",
        "うちわ",
        "カンペ",
        "双眼鏡",
        "タオル",
        "替えの電池",
        "ゲン担ぎ",
    ],
    "stage": [
        "双眼鏡",
        "上着",
        "静音タイプの袋",
    ],
    "meet": [
        "身分証の予備確認",
        "参加券",
        "メイク直し用品",
        "ネームタグ",
        "話したいことメモ",
    ],
    "online": [
        "イヤホン",
        "充電器",
        "通信環境の確認",
        "スクリーンショット保存先の確認",
        "見せたいもの",
    ],
}


# 天気別の持ち物リスト
WEATHER_ITEMS = {
    "sunny": [
        "日焼け止め",
        "水分",
    ],
    "rainy": [
        "折りたたみ傘",
        "ビニール袋",
        "タオル",
    ],
}


# 気温別の持ち物リスト
TEMPERATURE_ITEMS = {
    "normal": [],
    "hot": [
        "冷感シート",
        "飲み物",
        "日傘",
        "ハンディファン",
        "塩分タブレット",
        "汗拭きシート",
    ],
    "cold": [
        "カイロ",
        "マフラー",
        "手袋",
        "あたたかい飲み物",
    ],
}


# 遠征用の持ち物リスト
TRAVEL_ITEMS = [
    "宿泊予約の確認",
    "新幹線・飛行機・バスの予約確認",
    "着替え",
    "充電器",
    "寝巻",
    "スキンケア",
    "ヘアアイロン",
    "メイク用品",
    "コンタクト・眼鏡",
    "エコバッグ",
]


# 選択肢の表示名
EVENT_LABELS = {
    "live": "ライブ",
    "stage": "舞台",
    "meet": "接触イベント",
    "online": "オンラインイベント",
}


WEATHER_LABELS = {
    "sunny": "晴れ",
    "rainy": "雨",
}


TEMPERATURE_LABELS = {
    "normal": "普通",
    "hot": "暑い",
    "cold": "寒い",
}


def select_option(title, options):
    """選択肢を表示して、ユーザーに1つ選んでもらう関数"""
    print()
    print(title)

    keys = list(options.keys())

    for index, key in enumerate(keys, start=1):
        print(f"{index}. {options[key]}")

    while True:
        choice = input("番号を入力してください >> ")

        if choice.isdigit():
            choice_number = int(choice)

            if 1 <= choice_number <= len(keys):
                return keys[choice_number - 1]

        print("正しい番号を入力してください。")


def ask_yes_no(message):
    """y/nで答えてもらう関数"""
    while True:
        answer = input(f"{message} (y/n) >> ").lower()

        if answer == "y":
            return True

        if answer == "n":
            return False

        print("y または n で入力してください。")


def remove_duplicates(items):
    """重複した持ち物を削除する関数"""
    unique_items = []

    for item in items:
        if item not in unique_items:
            unique_items.append(item)

    return unique_items


def create_checklist(event_type, weather_type, temperature_type, is_travel):
    """条件に応じて持ち物リストを作る関数"""
    checklist = []

    checklist.extend(BASE_ITEMS)
    checklist.extend(EVENT_ITEMS[event_type])
    checklist.extend(WEATHER_ITEMS[weather_type])
    checklist.extend(TEMPERATURE_ITEMS[temperature_type])

    if is_travel:
        checklist.extend(TRAVEL_ITEMS)

    return remove_duplicates(checklist)


def create_output_text(event_type, weather_type, temperature_type, is_travel, checklist):
    """画面表示・保存用のテキストを作る関数"""
    today = datetime.now().strftime("%Y-%m-%d")

    travel_text = "あり" if is_travel else "なし"

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

    for item in checklist:
        lines.append(f"□ {item}")

    lines.extend(
        [
            "",
            "【メモ】",
            "□ チケット表示・座席・開演時間を確認する",
            "□ 帰りの交通手段を確認する",
            "□ 無理せず楽しむ",
        ]
    )

    return "\n".join(lines)


def save_output(text):
    """作成したチェックリストをoutputフォルダに保存する関数"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = output_dir / f"checklist_{now}.txt"

    file_path.write_text(text, encoding="utf-8")

    return file_path


def main():
    """アプリ全体の流れをまとめる関数"""
    print("================================")
    print("推し活現場もちものチェックリスト")
    print("================================")

    event_type = select_option(
        "現場タイプを選んでください",
        EVENT_LABELS,
    )

    weather_type = select_option(
        "天気を選んでください",
        WEATHER_LABELS,
    )

    temperature_type = select_option(
        "気温を選んでください",
        TEMPERATURE_LABELS,
    )

    is_travel = ask_yes_no("遠征ですか？")

    checklist = create_checklist(
        event_type,
        weather_type,
        temperature_type,
        is_travel,
    )

    output_text = create_output_text(
        event_type,
        weather_type,
        temperature_type,
        is_travel,
        checklist,
    )

    print()
    print(output_text)

    should_save = ask_yes_no("このチェックリストを保存しますか？")

    if should_save:
        file_path = save_output(output_text)
        print()
        print(f"保存しました：{file_path}")
    else:
        print()
        print("保存せずに終了しました。")


if __name__ == "__main__":
    main()