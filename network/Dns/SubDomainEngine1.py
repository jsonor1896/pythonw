from urllib.parse import urlparse

import requests
from lxml import etree


class SubDomainEngine1:
    """
    通过bing以及百度搜索引擎获取子网站子域名
    """

    @staticmethod
    def __get(search_engine:str, domain:str, func_format_url, func_parse_html):
        """
        向指定搜索引擎搜索获取特定域名下的所有子域名，模板函数
        :param search_engine: 搜索引擎
        :param domain: 域名
        :param func_format_url: url解析函数
        :param func_parse_html: html解析函数
        :return: 子域名的集合
        """
        Headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36 Edg/84.0.522.63',
            'referer': search_engine
        }

        subdomain_set = set()
        connect = requests.session()
        connect.get(search_engine, headers=Headers)

        for index in range(1, 10):
            url = func_format_url(domain=domain, page=index)
            html = connect.get(url, stream=True, headers=Headers, timeout=8).content
            subdomains = func_parse_html(html=html, connect=connect, headers=Headers)
            subdomain_set.update(subdomains)

        return subdomain_set

    @staticmethod
    def get_by_bingsearch(domain:str):
        """
        通过bing搜索引擎获取到网站的子域名
        :param domain: 主机域名
        :return: 子域名列表
        """
        def func_format_url(**kwargs):
            """
            格式化bing搜索的函数
            :param kwargs: 键值domain和page
            :return: 搜索链接地址
            """
            raw = 'https://www.bing.com/search?q=site%3a{url}&pq=site%3a{url}&first={first}&FORM=PERE'

            return raw.format(url=kwargs['domain'], first=(kwargs['page'] - 1) * 10)

        def func_parse_html(**kwargs):
            """
            解析html数据，返回当前页存在的所有子域名
            :return: 子域名集合
            """
            subs = set()
            html = etree.HTML(kwargs['html'])
            sub_domains = html.xpath("//ol[@id='b_results']/li/h2/a/@href")

            for item in sub_domains:
                url = urlparse(item)
                subs.add(url.scheme + '://' + url.netloc)

            return subs

        return SubDomainEngine1.__get('https://www.bing.com', domain, func_format_url, func_parse_html)

    @staticmethod
    def get_by_baidusearch(domain:str):
        """
        通过百度搜索引擎获取特定域名下的所有子域名
        :param domain: 域名
        :return: 子域名集合
        """
        def func_format_url(**kwargs):
            """
            格式化bing搜索的函数
            :param kwargs: 键值domain和page
            :return: 搜索链接地址
            """
            raw = 'https://www.baidu.com/s?wd=site%3A{url}&pn={pn}'

            return raw.format(url=kwargs['domain'], pn=(kwargs['page'] - 1) * 10)

        def func_parse_html(**kwargs):
            """
            解析html数据，返回当前页存在的所有子域名
            :param kwargs: html/connect
            :return: 子域名集合
            """
            subs = set()
            html = etree.HTML(kwargs['html'])
            sub_domains = html.xpath("//a[contains(@class, 'c-showurl')]/text()")
            sub_links   = html.xpath("//a[contains(@class, 'c-showurl')]/@href")

            for i in range(0, len(sub_domains)):
                sub = sub_domains[i]
                if SubDomainEngine1.has_chinese(sub):
                    response = kwargs['connect'].get(sub_links[i], stream=True, headers=kwargs['headers'], timeout=8)
                    url = urlparse(response.url)
                else:
                    url = urlparse(sub)

                if url.netloc:
                    if url.scheme:
                        subs.add(url.scheme + "://" + url.netloc)
                    else:
                        subs.add(url.netloc)
                else:
                    subs.add(url.path)

            return subs

        return SubDomainEngine1.__get('https://www.baidu.com', domain, func_format_url, func_parse_html)

    @staticmethod
    def has_chinese(string):
        """
        判断当前字符串中是否包含中文
        :param string: 需要被检查的字符串
        :return: 如果包含，返回True，否则返回False
        """
        for ch in string:
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False