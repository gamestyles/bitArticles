import random
import uuid

from django.core.management.base import BaseCommand

from article.models import Article, ArticleScore


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

    def handle(self, *args, **options):
        start_id = options['start_id']
        end_id = options['end_id']
        specified_score = options.get('score')
        score_count = options.get('count')

        articles = Article.objects.filter(id__gte=start_id, id__lte=end_id)
        if not articles.exists():
            self.stdout.write(self.style.WARNING(f"No articles found in the ID range {start_id} to {end_id}."))
            return

        for article in articles:
            for _ in range(score_count):
                # Generate a random score if no specific score is provided
                score_value = specified_score if specified_score else random.randint(1, 5)
                # Generate a random user ID
                user_id = uuid.uuid4()

                ArticleScore.objects.create(
                    article=article,
                    user_id=user_id,
                    score=score_value,
                )

                self.stdout.write(self.style.SUCCESS(
                    f"Assigned score {score_value} to Article ID {article.id} by User {user_id}."
                ))

        self.stdout.write(self.style.SUCCESS("Finished scoring articles."))
