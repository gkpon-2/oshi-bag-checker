import streamlit as st

from main import (
    EVENT_LABELS,
    WEATHER_LABELS,
    TEMPERATURE_LABELS,
    create_checklist,
    create_output_text,
)


# ページ全体の設定
st.set_page_config(
    page_title="推し活現場もちものチェックリスト",
    page_icon="👜",
    layout="wide",
)

# ホバー時のカーソルを調整するCSS
st.markdown(
    """
    <style>
    /* selectbox全体にカーソルを当てたとき */
    div[data-testid="stSelectbox"] {
        cursor: pointer;
    }

    div[data-testid="stSelectbox"] * {
        cursor: pointer;
    }

    /* checkbox全体にカーソルを当てたとき */
    div[data-testid="stCheckbox"] {
        cursor: pointer;
    }

    div[data-testid="stCheckbox"] * {
        cursor: pointer;
    }

    /* ボタンにカーソルを当てたとき */
    div[data-testid="stButton"] button {
        cursor: pointer;
    }

    /* ダウンロードボタンにカーソルを当てたとき */
    div[data-testid="stDownloadButton"] button {
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# タイトル
st.title("👜 推し活現場もちものチェックリスト")

# 説明文
st.write("現場タイプ・天気・気温・遠征有無に合わせて、持ち物リストを作成します。")


# 選択肢を画面表示用に作る
event_options = list(EVENT_LABELS.keys())
weather_options = list(WEATHER_LABELS.keys())
temperature_options = list(TEMPERATURE_LABELS.keys())


# 入力フォーム
with st.form("checklist_form"):
    st.subheader("条件を選択してください")

    # 横並びで選択欄を配置する
    col1, col2, col3 = st.columns(3)

    with col1:
        event_type = st.selectbox(
            "現場タイプ",
            event_options,
            format_func=lambda key: EVENT_LABELS[key],
        )

    with col2:
        weather_type = st.selectbox(
            "天気",
            weather_options,
            format_func=lambda key: WEATHER_LABELS[key],
        )

    with col3:
        temperature_type = st.selectbox(
            "気温",
            temperature_options,
            format_func=lambda key: TEMPERATURE_LABELS[key],
        )

    is_travel = st.checkbox("遠征あり")

    submitted = st.form_submit_button("チェックリストを作成する")


# 作成ボタンが押されたらチェックリストを表示する
if submitted:
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

    st.divider()

    st.subheader("✅ 持ち物チェックリスト")

    # 条件表示
    st.write("### ★条件")
    st.write(f"- 現場タイプ：{EVENT_LABELS[event_type]}")
    st.write(f"- 天気：{WEATHER_LABELS[weather_type]}")
    st.write(f"- 気温：{TEMPERATURE_LABELS[temperature_type]}")
    st.write(f"- 遠征：{'あり' if is_travel else 'なし'}")

    # チェックリスト表示
    st.write("### ★持ち物")

    for item in checklist:
        st.checkbox(item, key=f"item_{item}")

    # メモ表示
    st.write("### ★メモ")
    st.checkbox("チケット表示・座席・開演時間を確認する")
    st.checkbox("帰りの交通手段を確認する")
    st.checkbox("無理せず楽しむ")

    # テキストとしてダウンロードできるボタン
    st.download_button(
        label="チェックリストをtxtでダウンロード",
        data=output_text,
        file_name="oshi_bag_checklist.txt",
        mime="text/plain",
    )
else:
    st.info("条件を選んで「チェックリストを作成する」を押してください。")