from celery import group
from celery import shared_task
from celery.utils import log
from django.db.models import Avg
from decimal import Decimal

from .models import Article, ArticleScore

_logger = log.get_task_logger(__name__)


@shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def find_and_execute_article_stats_calculation_task():
    """
    Retrieves all article ids and groups the tasks and execute them to run and do calculations in parallel
    """
    articles = Article.objects.all().only("id")
    tasks = []
    # retrieve all ids to calculate
    for a in articles:
        tasks.append(calculate_article_stats_task.s(a.id))

    _logger.info(f"executing tasks of length: {len(tasks)} in group")
    # execute to calculate
    group(tasks).apply_async()


@shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def calculate_article_stats_task(article_id: int):
    """
    Calculates the average_score and total_score_count for a given article using article_id
    """
    available_scores = ArticleScore.objects.filter(article_id=article_id, is_suspicious=False)
    total_score_count = available_scores.count()
    average_score = available_scores.aggregate(Avg("score"))["score__avg"]
    decimal_avg = Decimal(average_score)

    updated_objs = Article.objects.filter(
        id=article_id
    ).update(
        total_score_count=total_score_count,
        average_score=decimal_avg
    )

    _logger.info(f"updated {updated_objs} objects")
