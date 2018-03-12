# !/usr/bin/env python
# -*- coding: utf-8 -*-


from elasticsearch import Elasticsearch


class ESClient(object):
    def __init__(self, hosts):
        self.hosts = hosts
        self.es = None
        self.is_init = False
        self.init()

    def init(self):
        if not isinstance(self.hosts, list):
            self.hosts = [self.hosts]
        try:
            self.es = Elasticsearch(hosts=self.hosts, timeout=10)
            if self.es.ping():
                self.is_init = True
        except Exception as error:
            raise Exception("{}".format(error))

    def stats(self):
        try:
            return self.es.cluster.stats()
        except Exception as error:
            raise Exception("{}".format(error))

    def search(self, index, doc_type, body, timeout="5s"):
        try:
            return self.es.search(index=index, doc_type=doc_type, body=body, ignore_unavailable=True, timeout=timeout)
        except Exception as error:
            raise Exception("{}".format(error))

    def get(self, index, doc_type, data_id):
        try:
            return self.es.get(index=index, doc_type=doc_type, id=data_id)
        except Exception as error:
            raise Exception("{}".format(error))

    def delete(self, index):
        try:
            self.es.indices.delete(index=index, ignore=[400, 404])
        except Exception as error:
            raise Exception("{}".format(error))


class ESGenerate(object):
    def __init__(self, must=None, should=None, must_not=None, include=None, size=0, from_size=None,
                 sort_dict=None, aggs_dict=None, multi_match=None, highlight=None):
        self.search_body = dict()
        self.query_must_condition = must if isinstance(must, list) else []
        self.query_should_condition = should if should and isinstance(should, list) else None
        self.query_must_not_condition = must_not if must_not and isinstance(must_not, list) else None
        self.include = include if isinstance(include, list) else []
        self.size = size if isinstance(size, int) else None
        self.from_size = from_size if isinstance(from_size, int) else None
        self.sort_dict = [sort_dict] if isinstance(sort_dict, dict) else None
        self.aggs_dict = aggs_dict if aggs_dict and isinstance(aggs_dict, dict) else None
        self.multi_match = multi_match if multi_match and isinstance(multi_match, dict) else None
        self.highlight = highlight if highlight and isinstance(highlight, dict) else None

    def __call__(self):
        return self.generate()

    def generate(self):
        if self.query_should_condition:
            self.query_must_condition += [{"bool": {"should": self.query_should_condition}}]
        if self.query_must_not_condition:
            self.query_must_condition += [{"bool": {"must_not": self.query_must_not_condition}}]

        if self.include:
            self.search_body["_source"] = self.include
        if self.from_size >= 0:
            self.search_body["from"] = self.from_size
        if self.sort_dict:
            self.search_body["sort"] = self.sort_dict
        if self.aggs_dict:
            self.search_body["aggs"] = self.aggs_dict
        if self.highlight:
            self.search_body["highlight"] = self.highlight
        if self.size is not None:
            self.search_body["size"] = self.size
        if self.multi_match:
            self.search_body["query"] = {"multi_match": self.multi_match}
        else:
            self.search_body["query"] = {"bool": {"must": self.query_must_condition}}

        return self.search_body
