# -*- coding: utf-8 -*-

import os
from wykop import WykopAPI
from time import sleep
import codecs
import sys

__author__ = 'michkraw'

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


class Parser:

    wykop = None
    archive_dir = os.path.dirname(os.path.realpath(__file__)) + "\\archive\\"
    keys = [
        ['EzpLlGp9HU', 'KaCGONIgTt'],
        ['uFKYHTqFFt', 'fAu2y6QTuV'],
    ]
    key_index = 0

    def __init__(self):
        self.get_key()
        # self.wykop.authenticate(login="InformacjaNieprawdziwaCCCL\VIII", accountkey="emuDtl1ye3UCOYAyBJOG")


    def parse(self):
        stop = False
        counter = 3120
        last_ok_page = 1
        while not stop:
            try:
                entries = self.wykop.search_entries(page=counter, q='')
            except:
                self.key_index += 1
                self.get_key()
                entries = self.wykop.search_entries(page=counter, q='')
            print "entries: ", len(entries)
            for entry in entries:
                self.archive_entry(entry)
            counter += 1
            print "counter: ", counter
            if len(entries) > 0 and entries[0]['author'] != None:
                print 'autor: ', entries[0]['author']
                last_ok_page = counter
            else:
                print 'ERROR, last ok was: %s' % last_ok_page
            sleep(0.5)


    def archive_entry(self, entry):
        self.append_to_archive(text=entry['body'], id=entry['id'], user=entry['author'])
        for comment in entry['comments']:
            self.archive_comment(comment)

    def archive_comment(self, comment):
        self.append_to_archive(text=comment['body'], id=comment['id'], user=comment['author'])

    def append_to_archive(self, text, id, user):
        dir_path = self.archive_dir + user
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path = dir_path + '\\' + format(id) + '.txt'

        mode = "w"
        # if os.path.exists(path):
        #     mode = "a"
        # else:
        with codecs.open(path, mode, "utf-8") as myfile:
            myfile.write(text)

    def get_key(self):
        self.wykop = WykopAPI(appkey=self.keys[self.key_index][0], secretkey=self.keys[self.key_index][1])


parser = Parser()
parser.parse()


