"""
streamlit_app.py

Streamlit を使った Web アプリ版の起動ファイル。
画面まわり（入力フォーム・チェックリスト表示・ダウンロード）を担当し、
チェックリストの中身を作る計算は oshi_bag パッケージに任せている。

【重要な設計ポイント：チェックすると初期画面に戻るバグの対策】
Streamlit は、ボタンやチェックボックスを操作するたびにスクリプトを上から再実行する。
form の送信ボタン（st.form_submit_button）が True を返すのは「送信した瞬間の1回だけ」なので、
「ボタンが押されたか」だけで表示を判定すると、チェックボックスを押した次の再実行で False に戻り、
作成済みのチェックリストが消えて初期画面に戻ってしまう。

そこで、作成したチェックリストを st.session_state（再実行をまたいで保持される保管場所）に保存し、
「セッションにチェックリストがあるか」で表示を判定するようにしている。
これにより、チェック操作をしてもチェックリストが保持される。
"""

import streamlit as st

from oshi_bag.data import (
    EVENT_LABELS,
    WEATHER_LABELS,
    TEMPERATURE_LABELS,
    MEMO_ITEMS,
)
from oshi_bag.checklist import create_checklist
from oshi_bag.output import create_output_text
from oshi_bag.custom_items import parse_custom_items


# ページ全体の設定（タブのタイトル・アイコン・横幅レイアウト）
st.set_page_config(
    page_title="推し活現場もちものチェックリスト",
    page_icon="👜",
    layout="wide",
)


# マウスを乗せたときのカーソルを指マークにするCSS（操作できる要素だと分かりやすくする）
st.markdown(
    """
    <style>
    div[data-testid="stSelectbox"] { cursor: pointer; }
    div[data-testid="stSelectbox"] * { cursor: pointer; }
    div[data-testid="stCheckbox"] { cursor: pointer; }
    div[data-testid="stCheckbox"] * { cursor: pointer; }
    div[data-testid="stButton"] button { cursor: pointer; }
    div[data-testid="stDownloadButton"] button { cursor: pointer; }
    </style>
    """,
    unsafe_allow_html=True,
)


# タイトルと説明文
st.title("👜 推し活現場もちものチェックリスト")
st.write("現場タイプ・天気・気温・遠征有無に合わせて、持ち物リストを作成します。")


# 選択肢のキー一覧を画面表示用に取り出す
event_options = list(EVENT_LABELS.keys())
weather_options = list(WEATHER_LABELS.keys())
temperature_options = list(TEMPERATURE_LABELS.keys())


# ------------------------------------------------------------
# 入力フォーム
# ------------------------------------------------------------
with st.form("checklist_form"):
    st.subheader("条件を選択してください")

    # 現場タイプ・天気・気温を横並び（3列）で配置する
    col1, col2, col3 = st.columns(3)

    with col1:
        # 現場タイプの選択欄（表示は日本語ラベル、中身はキー）
        event_type = st.selectbox(
            "現場タイプ",
            event_options,
            format_func=lambda key: EVENT_LABELS[key],
        )

    with col2:
        # 天気の選択欄
        weather_type = st.selectbox(
            "天気",
            weather_options,
            format_func=lambda key: WEATHER_LABELS[key],
        )

    with col3:
        # 気温の選択欄
        temperature_type = st.selectbox(
            "気温",
            temperature_options,
            format_func=lambda key: TEMPERATURE_LABELS[key],
        )

    # 遠征ありかどうかのチェック
    is_travel = st.checkbox("遠征あり")

    # 自由追加の持ち物入力欄（新機能）
    # 改行区切り・カンマ区切りのどちらでも書けるようにしている
    custom_text = st.text_area(
        "自由に追加したい持ち物（1行に1つ、またはカンマ区切り）",
        placeholder="例：推しのぬいぐるみ\nお守り、サイリウムの替え",
    )

    # 作成ボタン
    submitted = st.form_submit_button("チェックリストを作成する")


# ------------------------------------------------------------
# 作成ボタンが押されたとき：チェックリストを作って session_state に保存する
#
# ここで session_state に保存しておくことで、このあとチェックボックスを操作して
# スクリプトが再実行されても、作成済みのチェックリストが消えないようにする。
# ------------------------------------------------------------
if submitted:
    # 自由追加の入力テキストを、きれいな持ち物リストに変換する
    custom_items = parse_custom_items(custom_text)

    # 条件＋自由追加分をまとめてチェックリストを作る
    checklist = create_checklist(
        event_type,
        weather_type,
        temperature_type,
        is_travel,
        custom_items,
    )

    # ダウンロード用テキストを作る（自由追加分も含まれる）
    output_text = create_output_text(
        event_type,
        weather_type,
        temperature_type,
        is_travel,
        checklist,
    )

    # 再実行をまたいで保持したいデータを session_state に保存する
    st.session_state["checklist_result"] = {
        "event_type": event_type,
        "weather_type": weather_type,
        "temperature_type": temperature_type,
        "is_travel": is_travel,
        "checklist": checklist,
        "output_text": output_text,
    }


# ------------------------------------------------------------
# 表示の判定：session_state にチェックリストがあれば表示する
#
# 「submitted（押した瞬間だけTrue）」ではなく「保存済みデータの有無」で判定するのが
# バグ修正のポイント。これでチェック操作後の再実行でも表示が保たれる。
# ------------------------------------------------------------
result = st.session_state.get("checklist_result")

if result is None:
    # まだ一度も作成していない場合の案内
    st.info("条件を選んで「チェックリストを作成する」を押してください。")
else:
    st.divider()
    st.subheader("✅ 持ち物チェックリスト")

    # 条件のおさらいを表示する
    st.write("### ★条件")
    st.write(f"- 現場タイプ：{EVENT_LABELS[result['event_type']]}")
    st.write(f"- 天気：{WEATHER_LABELS[result['weather_type']]}")
    st.write(f"- 気温：{TEMPERATURE_LABELS[result['temperature_type']]}")
    st.write(f"- 遠征：{'あり' if result['is_travel'] else 'なし'}")

    # 持ち物のチェックボックスを表示する
    # key を付けることで、各チェックボックスの状態が再実行をまたいで保持される
    st.write("### ★持ち物")
    for item in result["checklist"]:
        st.checkbox(item, key=f"item_{item}")

    # メモ項目のチェックボックスを表示する
    st.write("### ★メモ")
    for memo in MEMO_ITEMS:
        st.checkbox(memo, key=f"memo_{memo}")

    # txt ダウンロードボタン（自由追加分を含む output_text を渡す）
    st.download_button(
        label="チェックリストをtxtでダウンロード",
        data=result["output_text"],
        file_name="oshi_bag_checklist.txt",
        mime="text/plain",
    )

    # 条件を変えて作り直したいとき用に、結果をリセットするボタン
    if st.button("条件を変えて作り直す"):
        # 保存していたチェックリストを消して初期状態に戻す
        del st.session_state["checklist_result"]
        st.rerun()
