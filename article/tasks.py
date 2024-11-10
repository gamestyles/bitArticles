from datetime import timedelta
from decimal import Decimal

from celery import group
from celery import shared_task
from celery.utils import log
from django.db.models import Avg, Sum
from django.utils import timezone

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


@shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def find_and_execute_article_suspicious_score_task():
    """
    Retrieves all article ids and groups the tasks and execute them to run and flag suspicious scores in parallel
    """
    articles = Article.objects.all().only("id")
    tasks = []
    # retrieve all ids to calculate
    for a in articles:
        tasks.append(flag_suspicious_user_scores.s(a.id))

    _logger.info(f"executing tasks of length: {len(tasks)} in group")
    # execute to calculate
    group(tasks).apply_async()


@shared_task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def flag_suspicious_user_scores(article_id: int):
    """
    Runs an algorithm to find and flag suspicious user scores.
    """
    # Define the time window for surge detection (e.g., 1 hour)
    time_threshold = timezone.now() - timedelta(hours=1)

    # Retrieve all article scores in the last hour
    recent_scores = ArticleScore.objects.filter(article_id=article_id, created_at__gte=time_threshold)
    _logger.info(f" len len len {recent_scores.count()}")

    # Extract score data and calculate mean and standard deviation
    total_score = recent_scores.aggregate(Sum("score"))["score__sum"]
    score_count = recent_scores.count()

    _logger.info(f" total {total_score}")

    if score_count == 0:
        _logger.info("No recent scores to analyze.")
        return

    # Calculate mean and standard deviation
    mean_score = total_score / score_count

    _logger.info(f"mean: {mean_score}")

    total_squared_diff = 0
    for score_entry in recent_scores:
        total_squared_diff += (score_entry.score - mean_score) ** 2

    standard_deviation = (total_squared_diff / score_count) ** 0.5

    # Define a z-score threshold for flagging suspicious scores
    threshold = 3  # Typically, a z-score > 3 or < -3 indicates an anomaly

    # Flag scores with z-scores > threshold or < -threshold
    suspicious_scores = []
    for score_entry in recent_scores:
        z_score = (score_entry.score - mean_score) / standard_deviation if standard_deviation != 0 else 0
        # if stddev becomes 0 for example all scores are same numbers, we decided that all of them are suspicious
        if abs(z_score) > threshold or z_score == 0:
            suspicious_scores.append(score_entry.id)

    affected_objs_count = ArticleScore.objects.filter(id__in=suspicious_scores).update(is_suspicious=True)
    _logger.info(f"affected scores {affected_objs_count}")
