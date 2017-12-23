# -*- coding: utf-8 -*-

import scrapy
from scrapy.http.request import Request

from yhanswers.items import QuestionItem


class YhAnswersSpider(scrapy.Spider):

    name = "YhAnswersSpider"
    start_urls = ["https://br.answers.yahoo.com/dir/index"]

    def start_requests(self):
        """Cria requisições com base no atributo start_urls.
            Returns:
                scrapy.Request requisição para página referente a cada url.
        """
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_categories)

    def parse_categories(self, response):
        """Obtém os links correspondentes as páginas de: Despesas, Receitas, Convênios, Licitação, Leis e Quadro Pessoal.
            Args:
                response: um objeto contendo o conteúdo html da página principal do portal da transparência.
            Retu rns:
                scrapy.Request requisição para página referente a cada critério.
        """
        main_categories = response.xpath("//*[contains(@href, 'dir/index?')]/@href").extract()

        for link in main_categories:
            url = "https://br.answers.yahoo.com%s" % link
            yield Request(url, callback=self.parse_sub_categories)

    def parse_sub_categories(self, response):

        sub_categories = response.xpath("//*[contains(@href, 'dir/index?')]/@href").extract()

        for link in sub_categories:
            url = "https://br.answers.yahoo.com%s" % link
            yield Request(url, callback=self.parse_question)


    def parse_question(self, response):
        questions_links = response.xpath("//*[contains(@href, 'question/index?qid')]/@href").extract()
        for link in questions_links:
            url = "https://br.answers.yahoo.com%s" % link
            yield Request(url, callback=self.extract_question)

    def extract_question(self, response):
        question = QuestionItem()
        question['title'] = response.xpath("//*[contains(@class, 'Fz-24 Fw-300 Mb-10')]/text()").extract_first()
        question['description'] = response.xpath("//*[contains(@class, 'D-n ya-q-full-text Ol-n')]/text()").extract_first()
        question['following'] = response.xpath("//*[contains(@class, 'follow-text')]/text()").extract_first()
        question['last_answers'] = response.xpath("//*[contains(@class, 'Mstart-75 Pos-r')]").extract_first()

        return question