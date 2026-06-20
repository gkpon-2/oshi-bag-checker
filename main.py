"""
main.py

コマンドライン版（CLI）の起動ファイル。
実際の処理は oshi_bag パッケージに分割してあるため、ここは起動するだけの薄い入口にしている。

使い方:
    python main.py
"""

from oshi_bag.cli import run_cli


# このファイルが直接実行されたときだけ、CLIアプリを起動する
if __name__ == "__main__":
    run_cli()
