from konlpy.tag import Hannanum
from collections import Counter

out = ['연합뉴스', '&apos']

def get_wordcount(titles, contents):
    #contents = contents.extend(titles)
    asdf = Hannanum()
    nouns = asdf.nouns(''.join(contents))

    filtered_nouns = [
        noun.replace('&quot;', '').replace('&apos;', '')
        for noun in nouns
        if '연합뉴스' not in noun and '현지시간' not in noun
    ]
    
    counts = Counter(filtered_nouns)
    
    return counts