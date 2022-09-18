import MeCab
import pandas as pd

def main():
    file = pd.read_csv('./data/lylics.csv')
    mecab = MeCab.Tagger("mecabrc")
    mecab.parse(' ')

    results = []
    for _, song in file.iterrows():
        node = mecab.parseToNode(song['歌詞'])
        while node:
            if node.surface == '':
                node = node.next
                continue
            feature = node.feature.split(',')
            pos = feature[0]
            if pos in ['名詞', '形容詞', '動詞', '副詞']:
                l = [node.surface] + list(song[['曲名', 'アルバム', '作曲者', '作詞者', '発売日']]) + feature
                results.append(l)
            node = node.next

    df = pd.DataFrame(results, columns = ['単語', '曲名', 'アルバム', '作曲者', '作詞者', '発売日'\
        , '品詞','品詞細分類1','品詞細分類2','品詞細分類3','活用型','活用形','原形','読み','発音'])
    df.to_csv('./data/parse.csv', index=False)

if __name__ == "__main__":
    main()
