import pandas as pd

from news.sina.rlnews import sinanews


def get_df(get_content=True, classification_count={'财经': 3, '股市': 3}):
    """
    '全部','国内','国际', '社会', '体育', '娱乐', '军事', '科技', '财经', '股市', '美股', '国内_国际', '国内_社会', '国际_社会', '国内国际社会'
    """
    dfs = []
    for k in classification_count:
        df = sinanews.get_rolling_news_csv(
            top=classification_count[k]
            , get_content=get_content
            , classify=k
        )
        dfs.append(df)
    final_df = pd.concat(dfs)
    return final_df


if __name__ == '__main__':
    df = get_df()
    print(df.columns)
    print(df)
