from fastapi import APIRouter
from api.utils.news_crawler import *
from api.utils.model import *
from api.utils.word_cloud import *

router = APIRouter()

@router.get("/api/news/korean")
def news_korean_emotions():
    news = get_korean_news()
    pos, negs = get_posnegs_gpt(news['title'])
    summary = get_summary_gpt(pos + negs)
    wordcount = get_wordcount(news['title'], news['content'])
    return {"korean_news": news, "positives": pos, "negatives": negs, "summary": summary, "wordcount": wordcount}