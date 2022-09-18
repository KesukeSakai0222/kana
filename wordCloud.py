from wordcloud import WordCloud

import pandas as pd
import sys
import re

def main():
    # words = data_select_all()
    words = data_select_album(sys.argv[1])
    # words = data_select_lylicist(sys.argv[1])
    # words = data_select_year(sys.argv[1])
    output(words, sys.argv[1])

def data_select_all():
    file = pd.read_csv('./data/parse.csv')
    # 原形のあるもののみを抜き出す
    words = ' '.join(file[file['原形'] != '*']['原形'])
    return words

def data_select_lylicist(lylicist):
    file = pd.read_csv('./data/parse.csv')
    file = file[file['原形'] != '*']
    words = ' '.join(file[file['作詞者'] == lylicist]['原形'])
    return words

def data_select_year(year):
    file = pd.read_csv('./data/parse.csv')
    file = file[file['原形'] != '*']
    words = ' '.join(file[file['発売日'].str.match(str(year) + '*')]['原形'])
    return words

def data_select_album(album):
    file = pd.read_csv('./data/parse.csv')
    file = file[file['原形'] != '*']
    words = ' '.join(file[file['アルバム'] == album]['原形'])
    return words

def output(words, name):
    fpath = './YuGothM.ttc'
    stop_words = {'そう', 'ない', 'いる', 'する', 'まま', 'よう', 'てる', 'なる', 'こと', 'もう', 'いい', 'ある', 'ゆく', 'れる', 'の', 'く', 'ん', 'られる'}
    # stop_words |= {'私', '君', 'あなた', 'わたし', 'キミ'}# , '誰'}

    wordcloud = WordCloud(background_color='white',
        font_path=fpath, width=1200, height=675, stopwords=set(stop_words)).generate(words)

    wordcloud.to_file('./data/'+ name +'.png')

if __name__ == "__main__":
    main()
