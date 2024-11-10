import random
import uuid
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import connection
from django.utils import timezone

from article.models import Article


class Command(BaseCommand):
    help = "Scores articles within a given article ID range with random or specified scores."

    def add_arguments(self, parser):
        parser.add_argument(
            'start_id', type=int, help='The starting article ID in the range'
        )
        parser.add_argument(
            'end_id', type=int, help='The ending article ID in the range'
        )
        parser.add_argument(
            '--score', type=int, choices=range(1, 6), help='Optional score to apply to each article (1 to 5)'
        )
        parser.add_argument(
            '--count', type=int, default=1, help='The number of scores to create for each article (default is 1)'
        )
        parser.add_argument(
            '--randomize-timestamp', action='store_true', help='Randomize the created_at timestamp before now()'
        )

    def handle(self, *args, **options):
        start_id = options['start_id']
        end_id = options['end_id']
        specified_score = options.get('score')
        score_count = options.get('count')
        randomize_timestamp = options['randomize_timestamp']

        articles = Article.objects.filter(id__gte=start_id, id__lte=end_id)
        if not articles.exists():
            self.stdout.write(self.style.WARNING(f"No articles found in the ID range {start_id} to {end_id}."))
            return

        # Prepare SQL query template
        sql_insert = """
            INSERT INTO article_articlescore (article_id, user_id, score, created_at, is_suspicious)
            VALUES (%s, %s, %s, %s, %s)
        """

        # using raw sql to not change auto_now_add on created_at
        with connection.cursor() as cursor:
            for article in articles:
                for _ in range(score_count):
                    # Generate a random score if no specific score is provided
                    score_value = specified_score if specified_score else random.randint(1, 5)
                    # Generate a random user ID
                    user_id = uuid.uuid4()
                    # Randomize the created_at timestamp if the flag is set
                    created_at = timezone.now()
                    if randomize_timestamp:
                        random_days = random.randint(0, 30)  # Random date within the last 30 days
                        random_seconds = random.randint(0, 86400)  # Random time within a day
                        created_at -= timedelta(days=random_days, seconds=random_seconds)

                    # Execute raw SQL insert
                    cursor.execute(sql_insert, [
                        article.id,                  # article_id
                        str(user_id),                # user_id as string
                        score_value,                 # score
                        created_at,                  # created_at timestamp
                        False                        # is_suspicious
                    ])

                    self.stdout.write(self.style.SUCCESS(
                        f"Assigned score {score_value} to Article ID {article.id} by User {user_id} at {created_at}."
                    ))

        self.stdout.write(self.style.SUCCESS("Finished scoring articles."))
