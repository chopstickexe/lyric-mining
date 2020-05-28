import glob
import re
from typing import List, Tuple

import pandas as pd


def __read(path: str) -> Tuple[List[str], List[str], List[str]]:
    titles = []
    singers = []
    lines = []
    with open(path, mode="r", encoding="utf-8") as f:
        title = ""
        singer = ""
        for i, line in enumerate(f):
            line = line.rstrip("\n").strip()
            if len(line) == 0:
                continue
            if i == 0:
                title = line
            elif i == 2:
                singer = re.sub(r'歌手　|アーティスト　', '', line)
            elif i > 4:
                line = re.sub(r'【.+】', '', line)  # 歌割を消す
                titles.append(title)
                singers.append(singer)
                lines.append(line)
    return titles, singers, lines


def to_df(raw_data_pat: str) -> pd.DataFrame:
    all_titles = []
    all_singers = []
    all_lines = []
    for file in glob.glob(raw_data_pat):
        titles, singers, lines = __read(file)
        all_titles.extend(titles)
        all_singers.extend(singers)
        all_lines.extend(lines)
    return pd.DataFrame(
        data={"title": all_titles, "singer": all_singers, "line": all_lines}
    )


def main():
    df = to_df("data/raw/*.txt")
    print(df.shape)


if __name__ == "__main__":
    main()
