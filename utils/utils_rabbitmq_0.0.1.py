# !/usr/bin/env python
# -*- coding: utf-8 -*-


import pika
import requests
import fnmatch


class RabbitmqUtil(object):
    def __init__(self, queue_host):
        self.queue_host = queue_host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(queue_host))
        self.channel = self.connection.channel()

    def bind_queues(self, exchange_name, queue_list):
        try:
            self.channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
            for single_queue in queue_list:
                self.channel.queue_declare(queue=single_queue)
                self.channel.queue_bind(exchange=exchange_name, queue=single_queue)
            return True
        except None, err:
            return False

    def write_queue(self, exchange_name, content):
        try:
            self.channel.basic_publish(exchange=exchange_name, routing_key='', body=content)
            return True
        except None, err:
            return False

    def read_queue(self, queue_name):
        method_frame, header_frame, body = self.channel.basic_get(queue=queue_name, no_ack=True)
        return method_frame, body

    def delete_queue(self, queue_name):
        try:
            self.channel.queue_delete(queue=queue_name)
            return True
        except:
            return False

    def delete_exchange(self, exchange_name):
        try:
            self.channel.exchange_delete(exchange=exchange_name)
            return True
        except:
            return False

    def get_queue_dict(self, prefix=None, suffix=None):
        queue_dict = {}
        api_url = 'http://%s:15672/api/queues' % self.queue_host
        try:
            r = requests.get(api_url, auth=('guest', 'guest'))
            result_json = r.json()
            for line in result_json:
                queue_name = str(line['name']).strip()
                if (not prefix) and (not suffix):
                    queue_dict[queue_name] = int(line['messages']) if 'messages' in line else 0
                elif not suffix:
                    pattern = '%s*' % prefix
                    if fnmatch.fnmatch(queue_name, pattern):
                        queue_dict[queue_name] = int(line['messages']) if 'messages' in line else 0
                    else:
                        continue
                elif not prefix:
                    pattern = '*%s' % suffix
                    if fnmatch.fnmatch(queue_name, pattern):
                        queue_dict[queue_name] = int(line['messages']) if 'messages' in line else 0
                    else:
                        continue
                else:
                    prefix_pattern = '%s*' % prefix
                    suffix_pattern = '*%s' % suffix
                    if fnmatch.fnmatch(queue_name, prefix_pattern) and fnmatch.fnmatch(queue_name, suffix_pattern):
                        queue_dict[queue_name] = int(line['messages']) if 'messages' in line else 0
                    else:
                        continue
            return 0, queue_dict
        except:
            return 1, queue_dict

    def get_messages_count(self):
        messages_count = None
        api_url = 'http://%s:15672/api/overview' % self.queue_host
        try:
            r = requests.get(api_url, auth=('guest', 'guest'))
            result_json = r.json()
            messages_count = result_json['queue_totals']['messages'] \
                if ('queue_totals' in result_json) and ('messages' in result_json['queue_totals']) else None
            return messages_count
        except:
            return messages_count

    def close(self):
        self.connection.close()
