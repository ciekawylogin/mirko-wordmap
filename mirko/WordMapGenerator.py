# -*- coding: utf-8 -*-

import codecs
from wordcloud import WordCloud
import os
import pyimgur

__author__ = 'michkraw'


class WordmapGenerator:
    blacklist = [u'w', u'że', u'na', u'się', u'nie', u'tak', u'ale', u'u', u'co', u'z']
    imgur_client_id = '49b3b1438d32d3e'

    def generate(self, user):
        dirname = os.path.dirname(os.path.realpath(__file__))
        user_dir = dirname + '\\archive\\' + user
        text = ''
        entry_count = 0
        comment_count = 0
        for file_name in os.listdir(user_dir):
            if file_name.startswith('1'):
                entry_count += 1
            elif file_name.startswith('4'):
                comment_count += 1
            with codecs.open(user_dir + '\\' + file_name, 'r', "utf-8") as file:
                file_contents = file.read()
                text += '\n' + file_contents

        # for word in self.blacklist:
        #     text = text.replace(word, '')

        wordcloud = WordCloud(width=1280, height=860, max_font_size=150, font_path=dirname+'\\Aller_Lt.ttf')
        a = wordcloud.generate(text)
        img = a.to_image()
        image_location = dirname + '\\img\\' + user + '.png'
        img.save(image_location, format='png')

        imgur = pyimgur.Imgur(self.imgur_client_id)
        uploaded_image = imgur.upload_image(image_location, title="Chmura słów użytkownika " + user + " na mirko (wykop.pl/mikroblog)")
        return u"@" + user + ": " + uploaded_image.link + " (" + format(uploaded_image.size/1024) + " kb, wygenerowano z " + format(entry_count) + u" wpisów i " + format(comment_count) + u" komentarzy do wpisów)" + ""

ludzie_txt = "  powazny, CalkowicieRandomowyNick, Wyrazisty, marianoitaliano, OPZK, Ajen, Tasde, Typowy_polak, Jewptylianin, hazawwin, endryoou, rasmor, MrEid"
ludzie = ludzie_txt.split(',')
for czlowiek in ludzie:
    generator = WordmapGenerator()
    try:
        print generator.generate(user=czlowiek.strip())
    except:
        print '@' + czlowiek.strip() + ': pusto'
