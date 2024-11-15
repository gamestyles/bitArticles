from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


class Article(models.Model):
    title = models.CharField(null=False, blank=False, max_length=255, help_text=_("the title of the article"))
    created_at = models.DateTimeField(auto_now_add=True)
    average_score = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True, help_text=_("Average score that users gave the article"))
    total_score_count = models.IntegerField(null=True, blank=True, help_text=_("total number of users gave score"))

    def __str__(self):
        return self.title


class ArticleScore(models.Model):
    """
    User scores articles
    """
    article = models.ForeignKey(Article, on_delete=models.DO_NOTHING, help_text=_("score related to an article"))
    user_id = models.UUIDField(null=False, blank=False, db_index=True, help_text=_("the user id who scored"))
    score = models.PositiveSmallIntegerField(
        null=False, blank=False, validators=[MaxValueValidator(5), MinValueValidator(1)],
        help_text=_("the score that can be between 1 to 5")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_suspicious = models.BooleanField(default=False, help_text=_("the score can be suspicious based on user activity"))
