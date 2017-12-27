# -*- coding: utf-8 -*-

from scrapy.http.response.html import HtmlResponse

from w3lib.html import remove_tags_with_content, remove_tags
from bs4 import BeautifulSoup, Comment


class HtmlUtil(object):

    @staticmethod
    def remove_all_tags(html):
        """Remove all tags html code
            Args:
                html: html code for remove tags
            Returns:
                text without html tags.
        """
        soup = BeautifulSoup(html)
        return soup.get_text()

    @staticmethod
    def converte_codigo_font_html_response(source, url_pagina):
        """Convert code string in scrapy.Response
            Args:
                source: Source html code.
                url_pagina: URL of page extracted
            Returns:
                Object scrapy.Response.
        """
        return HtmlResponse(url=url_pagina, body=source, encoding='utf-8')

    @staticmethod
    def clean_html(html):
        """Remove tags scripts, style, comments, footer and links of html code
            Args:
                html: html code for remove tags and comments
            Returns:
                html with tags and comments removed
        """
        soup = BeautifulSoup(html)
        for script in soup(["script", "style", "footer", "link"]):
            script.extract()

        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        text = soup.prettify()

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text