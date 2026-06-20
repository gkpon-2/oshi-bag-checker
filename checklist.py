"""
checklist.py

このモジュールは「チェックリストの組み立てロジック」を担当する。
選ばれた条件（現場タイプ・天気・気温・遠征有無）と、ユーザーが自由に追加した持ち物をもとに、
重複を取り除いた1本の持ち物リストを作る。

データそのもの（data.py）とは分離してあり、ここでは「どう組み合わせるか」だけを扱う。
"""

from oshi_bag.data import (
    BASE_ITEMS,
    EVENT_ITEMS,
    WEATHER_ITEMS,
    TEMPERATURE_ITEMS,
    TRAVEL_ITEMS,
)


def remove_duplicates(items):
    """
    重複した持ち物を取り除く関数。

    同じ持ち物が複数の条件から追加されることがあるため（例：タオルはライブと雨の両方）、
    先に出てきた順番を保ったまま、2回目以降の同じ持ち物を捨てる。
    """
    unique_items = []

    for item in items:
        # まだ追加していない持ち物だけをリストに入れる
        if item not in unique_items:
            unique_items.append(item)

    return unique_items


def create_checklist(
    event_type,
    weather_type,
    temperature_type,
    is_travel,
    custom_items=None,
):
    """
    条件に応じて持ち物リストを作る関数。

    引数:
        event_type:       現場タイプのキー（live / stage / meet / online）
        weather_type:     天気のキー（sunny / rainy）
        temperature_type: 気温のキー（normal / hot / cold）
        is_travel:        遠征ありかどうか（True / False）
        custom_items:     ユーザーが自由に追加した持ち物のリスト（省略可）

    戻り値:
        重複を取り除いた持ち物リスト
    """
    checklist = []

    # 1. まず基本の持ち物を入れる
    checklist.extend(BASE_ITEMS)

    # 2. 現場タイプに応じた持ち物を足す
    checklist.extend(EVENT_ITEMS[event_type])

    # 3. 天気に応じた持ち物を足す
    checklist.extend(WEATHER_ITEMS[weather_type])

    # 4. 気温に応じた持ち物を足す
    checklist.extend(TEMPERATURE_ITEMS[temperature_type])

    # 5. 遠征ありなら遠征用の持ち物を足す
    if is_travel:
        checklist.extend(TRAVEL_ITEMS)

    # 6. ユーザーが自由に追加した持ち物があれば最後に足す
    if custom_items:
        checklist.extend(custom_items)

    # 7. 重複を取り除いて返す
    return remove_duplicates(checklist)
