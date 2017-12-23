# -*- coding: utf-8 -*-

from scrapy.http.response.html import HtmlResponse

from w3lib.html import remove_tags_with_content, remove_tags
from bs4 import BeautifulSoup, Comment


class HtmlUtil(object):

    @staticmethod
    def remove_tag_html(nome_tag, source):
        """Remove uma tag do código fonte passado
            Args:
                nome_tag: nome da tag html que deseja remover.
                source: código fonte ao qual a tag será removida
            Returns:
                código fonte sem a presença da tag html passada.
        """
        return remove_tags_with_content(source, (nome_tag,))

    @staticmethod
    def converte_codigo_font_html_response(source, url_pagina):
        """Converte código fonte html para o padrão Response reconhecido pelo crawler
            Args:
                source: código fonte que deve ser convertido para Response.
                url_pagina: URL do código fonte extraído.
            Returns:
                Objeto Response.
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