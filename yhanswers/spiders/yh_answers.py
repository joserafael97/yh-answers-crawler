# -*- coding: utf-8 -*-

import scrapy
from scrapy.http.request import Request

from yhanswers.items import QuestionItem
from yhanswers.util import HtmlUtil


class YhAnswersSpider(scrapy.Spider):

    name = "YhAnswersSpider"
    start_urls = ["https://br.answers.yahoo.com/dir/index?sid=0"]

    def start_requests(self):
        """create request with base in start_urls.
            Returns:
                scrapy.Request request to parse_categories.
        """
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse_categories)

    def parse_categories(self, response):
        """Scrapy links to categories.
            Args:
                response: response with html code.
            Returns:
                scrapy.Request
        """
        main_categories = response.xpath("//*[contains(@href, 'dir/index?')]/@href").extract_first()
        # for link in main_categories:
        url = "https://br.answers.yahoo.com%s" % main_categories
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
        description = response.xpath("//*[contains(@class, 'ya-q-full-text Ol-n')]/text()").extract_first()
        if not description:
            description = response.xpath("//*[contains(@class, 'ya-q-text')]/text()").extract_first()
        question['description'] = description
        following = response.xpath("//*[contains(@class, 'follow-text')]/text()").extract_first()
        if "Seguir" in following:
            following = 0
        else:
            following = following.replace('seguindo', '').replace(' ', '')
        question['following'] = following
        lasts_answers = response.xpath("//*[contains(@class, 'answer-detail Fw-n')]").extract()
        filter_answers = []
        for answer in lasts_answers:
            filter_answers.append(HtmlUtil.remove_all_tags(answer))
        question['last_answers'] = filter_answers
        question['answers_number'] = response.xpath('//*[@class="D-n"]/text()').extract_first()
        return question