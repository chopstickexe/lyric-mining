# %%
# Exploratory data analysis using VSCode interactive Python window
from txt2txt_ebc import data_process
df = data_process.to_df("../data/raw/ebc/*.txt")
df.shape

# %%
df.head()

# %%
df[df['singer'] == 'ももいろクローバーZ'].shape

# %%
df[df['singer'] == '私立恵比寿中学'].shape

# %%
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSKeepFilter
a = Analyzer(token_filters=[POSKeepFilter(['名詞'])])
def analyze(txt: str):
    tokens = []
    for token in a.analyze(txt):
        tokens.append(token.base_form)
    return ' '.join(tokens)

df['wakati_line'] = df['line'].apply(analyze)
df['wakati_line']

# %%
import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud
def count_tf(df):
    words=df['wakati_line'].str.split(expand=True).stack().value_counts().to_dict()
    return words

def get_unique_words(words_with_spaces):
    unique_words = set(words_with_spaces.split())
    return ' '.join(unique_words)

def count_df(df):
    doc = df.groupby(['title'])['wakati_line'].apply(' '.join)
    doc = doc.apply(get_unique_words)
    words = doc.str.split(expand=True).stack().value_counts().to_dict()
    return words

def remove_stopwords(words):
    del_keys = set()
    for word in words.keys():
        # ひらがなカタカナ一文字と括弧は除外
        if len(word) < 2 and re.match(r'[ぁ-んァ-ン\(\)\[\]]', word) :
            del_keys.add(word)
    for word in del_keys:
        words.pop(word, None)
    return words

def draw_wordcloud(words, **kwds):
    wc = WordCloud(font_path="../.fonts/NotoSansCJKjp-Regular.otf", **kwds)
    wc.generate_from_frequencies(words)
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

# %%
words = count_tf(df[df['singer'] == '私立恵比寿中学'])
print(len(words))
remove_stopwords(words)
print(len(words))
draw_wordcloud(words, width=800, height=600, max_words=100, colormap='summer') 

# %%
words = count_tf(df[df['singer'] == 'ももいろクローバーZ'])
print(len(words))
remove_stopwords(words)
print(len(words))
draw_wordcloud(words, width=800, height=600, max_words=100, colormap='spring') 

# %%
words = count_tf(df[df['singer'] == 'Mr.Children'])
print(len(words))
remove_stopwords(words)
print(len(words))
draw_wordcloud(words, width=800, height=600, max_words=100, colormap='winter') 

# %%
df[(df['singer'] == 'Mr.Children') & (df['line'].str.contains('誰'))]

# %%
df.head

# %%
df[df['singer'] == '私立恵比寿中学']['line'].to_csv('ebc.csv', index=False, header=False)

# %%
