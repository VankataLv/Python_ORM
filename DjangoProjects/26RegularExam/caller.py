import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Review, Article
from django.db.models import Q, Sum, Count, Avg


# Create queries within functions
def get_authors(search_name=None, search_email=None):
    query_name = Q(full_name__icontains=search_name)
    query_email = Q(email__icontains=search_email)

    if search_name is not None and search_email is not None:
        query = Q(query_name & query_email)

    elif search_name is not None and search_email is None:
        query = query_name

    elif search_name is None and search_email is not None:
        query = query_email

    else:
        return ""

    authors = Author.objects.filter(query).order_by('-full_name')

    if authors:
        result = []
        for author in authors:
            if author.is_banned:
                status = 'Banned'
            else:
                status = 'Not Banned'
            result.append(f"Author: {author.full_name}, email: {author.email}, status: {status}")

        return '\n'.join(result)

    else:
        return ""


def get_top_publisher():
    author = Author.objects.get_authors_by_article_count().first()
    if not author or author.article_count == 0:
        return ""
    return f"Top Author: {author.full_name} with {author.article_count} published articles."


def get_top_reviewer():
    reviewer = Author.objects.annotate(
        review_count=Count('author_reviews')
    ).order_by(
        '-review_count', 'email'
    ).first()

    if not reviewer or reviewer.review_count == 0:
        return ""

    return f"Top Reviewer: {reviewer.full_name} with {reviewer.review_count} published reviews."


# --------------------------------------------------------------------------------------------------------
def get_latest_article():
    latest_article = Article.objects.prefetch_related('authors', 'article_reviews').order_by('published_on').last()

    if not latest_article:
        return ""

    authors = [a.full_name for a in latest_article.authors.order_by('full_name')]
    review_count = latest_article.article_reviews.count()

    if review_count != 0:
        avg_rating = sum(r.rating for r in latest_article.article_reviews.all())/review_count
    else:
        avg_rating = 0
    return f"The latest article is: {latest_article.title}. "\
           f"Authors: {', '.join(authors)}. "\
           f"Reviewed: {review_count} times. Average Rating: {avg_rating:.2f}."


def get_top_rated_article():
    article = Article.objects.prefetch_related('article_reviews').annotate(
        review_count=Count('article_reviews__rating'),
        avg_rating=Avg('article_reviews__rating'),
    ).order_by('-avg_rating', 'title').first()

    if not article or article.review_count == 0:
        return ""

    return f"The top-rated article is: {article.title}, with an average rating of {article.avg_rating:.2f}, "\
           f"reviewed {article.review_count} times."


def ban_author(email=None):
    author_to_ban = (Author.objects.prefetch_related('author_reviews')
                     .filter(email__exact=email)
                     .first())

    if author_to_ban is None or email is None:
        return "No authors banned."

    author_to_ban.is_banned = True
    num_reviews = author_to_ban.author_reviews.count()
    author_to_ban.save()
    author_to_ban.author_reviews.all().delete()
    return f"Author: {author_to_ban.full_name} is banned! {num_reviews} reviews deleted."

