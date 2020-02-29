# -*- coding: utf-8 -*-

"""
新浪新闻数据接口
"""

import re
import json
import random
import lxml.html
import lxml.etree
import numpy as np
import pandas as pd
from datetime import datetime

from news.sina.rlnews import sina_constants as cts
from news.sina.rlnews.utils.disk_cache import DiskCache
from news.sina.rlnews.utils.downloader import Downloader

DEBUG = True


class SinaNewsCrawller:

    def __init__(self):
        self.__no_cache_downloader = Downloader(cache=None)
        self.__disk_cache_downloader = Downloader(cache=DiskCache())

    def get_rolling_news_bypage(self, page_from, page_to, get_content=True, classify=None):
        '''
        获取新浪滚动新闻，每页50条新闻
        :param page_from: 从第几页开始
        :param page_to: 到第几页
        :param get_content: bool, 是否获取新闻内容，默认为True
        :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
        :return: pd.DataFrame, 新闻信息 DataFrame
        '''

        pages = np.arange(page_from, page_to)
        nums = [cts.max_num_per_page] * len(pages)
        pages_nums = dict(zip(pages, nums))
        return self.__get_rowlling_news(classify, pages_nums, get_content)

    def get_rolling_news_bycount(self, count=50, get_content=True, classify=None):
        """
        获取新浪滚动新闻
        :param cnt: int, 获取的滚动新闻条数，默认为50
        :param get_content: bool, 是否获取新闻内容，默认为True
        :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
        :return: pd.DataFrame, 新闻信息数据框
        """

        nums = [cts.max_num_per_page] * (count // cts.max_num_per_page)
        last_page_num = count % cts.max_num_per_page
        if last_page_num:
            nums += [last_page_num]

        pages = np.arange(1, 1 + len(nums))
        pages_nums = dict(zip(pages, nums))
        return self.__get_rowlling_news(classify, pages_nums, True)

    def __get_lidclassify(self, classify):
        lid = cts.classification2lid.get(classify, '2509')
        classify = cts.lid2classification[lid]
        return lid, classify

    def __get_rowlling_news(self, classify, pages_nums, get_content=True):
        if classify:
            assert classify in cts.classifications, (
                '请设置 classify 为 {}中的一个'.format(cts.classifications)
            )
        lid, classify = self.__get_lidclassify(classify)

        df_data = []
        for item in pages_nums.items():
            r = random.random()
            url = cts.template_url.format(lid, item[1], item[0], r)
            response = self.__no_cache_downloader(url)
            response_dict = json.loads(response)
            data_list = response_dict['result']['data']

            for data in data_list:
                # with open('./cache/' + data['title'], 'x') as json_file:
                # json.dump(data, json_file)
                ctime_raw = data['ctime']
                ctime = datetime.fromtimestamp(int(data['ctime']))
                ctime = datetime.strftime(ctime, '%Y-%m-%d %H:%M')
                url = data['url']
                row = [
                    classify
                    , data['title']
                    , ctime_raw
                    , ctime
                    , url
                    , data['wapurl']
                    , data['media_name']
                    , data['keywords']
                    , data['intro']
                    # , data['level']
                ]
                if get_content:
                    row.append(self.__get_news_content(url))
                df_data.append(row)

        df = pd.DataFrame(df_data, columns=cts.columns if get_content else cts.columns[:-1])
        return df

    def __get_news_content(self, url):
        """
        获取新闻内容
        :param url: str, 新闻链接
        :return: str, 新闻内容
        """
        content = ''
        try:
            text = self.__disk_cache_downloader(url)
            html = lxml.etree.HTML(text)
            res = html.xpath('//*[@id="artibody" or @id="article"]//p')
            p_str_list = [lxml.etree.tostring(node).decode('utf-8') for node in res]
            p_str = ''.join(p_str_list)
            html_content = lxml.html.fromstring(p_str)
            content = html_content.text_content()
            # 清理未知字符和空白字符
            content = re.sub(r'\u3000', '', content)
            content = re.sub(r'[ \xa0?]+', ' ', content)
            content = re.sub(r'\s*\n\s*', '\n', content)
            content = re.sub(r'\s*(\s)', r'\1', content)
            content = content.strip()
        except Exception as e:
            print('get_news_content(%s) error:' % url, e)
        return content


'''
def get_rolling_news_url(top=50, classify=None):
    """
    获取新浪滚动新闻url
    :param top: int, 获取的滚动新闻条数，默认为50
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :return: pd.DataFrame, 新闻信息数据框
    """
    if classify:
        assert classify in cts.classifications, (
            '请设置 classify 为 {}中的一个'.format(cts.classifications)
        )

    lid = cts.classification2lid.get(classify, '2509')
    num_list = [cts.max_num_per_page] * (top // cts.max_num_per_page)
    last_page_num = top % cts.max_num_per_page
    if last_page_num:
        num_list += [last_page_num]

    urls = []
    for page, num in enumerate(num_list, start=1):
        r = random.random()
        url = cts.template_url.format(lid, num, page, r)
        response = no_cache_downloader(url)
        response_dict = json.loads(response)
        data_list = response_dict['result']['data']
        for data in data_list:
            url = data['url']
            urls.append(url)
    return urls
'''

'''
def get_rolling_news_csv(top=50, get_content=True, classify=None, path=None):
    """
    获取新浪滚动新闻并保存成csv文件
    :param top: int, 获取的滚动新闻条数，默认为50
    :param get_content: bool, 是否获取新闻内容，默认为True
    :param classify: str, 获取的滚动新闻的类别，默认为None，即"2509:全部"
    :param path: str, 文件保存路径
    """
    df = get_rolling_news(top=top, get_content=get_content, classify=classify)
    return df
    # if not path:
    # path = 'news.csv'
    # df.to_csv(path, index=False, encoding='utf-8')
'''

if __name__ == '__main__':
    # get_rolling_news_csv(top=5, get_content=True, classify='全部')
    pass
