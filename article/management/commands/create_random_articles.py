import random

from django.core.management.base import BaseCommand

from article.models import Article


class Command(BaseCommand):
    help = "Creates a specified number of articles with random titles."

    def add_arguments(self, parser):
        parser.add_argument(
            'number', type=int, help='The number of articles to create'
        )

    def handle(self, *args, **options):
        number_of_articles = options['number']
        titles = [
            "Mastering Python: Tips and Tricks",
            "The Ultimate Guide to Machine Learning",
            "A Deep Dive into RESTful APIs",
            "Top 10 Web Development Practices in 2024",
            "Database Optimization Techniques",
            "Building Scalable Web Applications",
            "Understanding the Basics of Data Science",
            "Frontend Frameworks: What to Choose",
            "Backend Best Practices for Developers",
            "Secrets of Successful API Design",
            "Debugging Strategies for Complex Codebases",
            "Optimizing SQL Queries for Performance",
            "The Power of Python in Data Analysis",
            "A Beginner's Guide to AI and Machine Learning",
        ]

        for _ in range(number_of_articles):
            title = random.choice(titles) + f" #{random.randint(1, 10000)}"
            Article.objects.create(title=title)
            self.stdout.write(self.style.SUCCESS(f"Article '{title}' created."))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {number_of_articles} articles."))
