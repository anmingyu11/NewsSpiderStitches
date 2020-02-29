import pandas as pd

from news.sina.rlnews.sinanews import SinaNewsCrawller
import numpy as np


def get_news_df_bypage(page_from, page_to, get_content=True, classifications=['财经', '股市']):
    """
    '全部'
    ,'国内'
    ,'国际'
    , '社会', '体育', '娱乐', '军事', '科技', '财经', '股市', '美股', '国内_国际', '国内_社会', '国际_社会', '国内国际社会'
    """
    snc = SinaNewsCrawller()
    dfs = []
    for k in classifications:
        df = snc.get_rolling_news_bypage(
            page_from
            , page_to
            , get_content=get_content
            , classify=k
        )
        dfs.append(df)
    final_df = pd.concat(dfs)
    return final_df


if __name__ == '__main__':
    d = dict(zip([1,2,3],[4,5,6]))
    for item in d.items():
        print(item[0],':',item[1])
    df = get_news_df_bypage(1,2)
    print(df.columns)
    print(df)
