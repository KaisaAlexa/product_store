from datetime import timedelta

from django.core.management import BaseCommand
from django.utils import timezone

from blogapp.models import Article, Author, Category, Tag


class Command(BaseCommand):
    """
    Creates test articles for blogapp using bulk_create.
    """

    def handle(self, *args, **options):
        self.stdout.write("Creating test data for blogapp...")

        Article.objects.all().delete()
        Author.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

        authors = Author.objects.bulk_create([
            Author(name="John Doe", bio="Writer and journalist"),
            Author(name="Jane Smith", bio="Tech blogger"),
            Author(name="Alex Johnson", bio="Travel enthusiast"),
        ])

        categories = Category.objects.bulk_create([
            Category(name="Technology"),
            Category(name="Travel"),
            Category(name="Science"),
        ])

        tags = Tag.objects.bulk_create([
            Tag(name="python"),
            Tag(name="django"),
            Tag(name="web"),
            Tag(name="tutorial"),
            Tag(name="news"),
        ])

        now = timezone.now()
        articles_data = [
            (
                "Getting Started with Django",
                "Django is a high-level Python web framework...",
                authors[0],
                categories[0],
                [tags[0], tags[1], tags[3]],
                now - timedelta(days=5),
            ),
            (
                "Optimizing Database Queries",
                "Learn how to use select_related, prefetch_related, and defer...",
                authors[1],
                categories[0],
                [tags[0], tags[2], tags[3]],
                now - timedelta(days=3),
            ),
            (
                "Weekend Trip to the Mountains",
                "A short guide to planning a hiking trip...",
                authors[2],
                categories[1],
                [tags[4]],
                now - timedelta(days=1),
            ),
            (
                "Latest Discoveries in Physics",
                "Scientists have made new observations about quantum systems...",
                authors[0],
                categories[2],
                [tags[4], tags[3]],
                now,
            ),
        ]

        articles = Article.objects.bulk_create([
            Article(
                title=title,
                content=content,
                author=author,
                category=category,
                pub_date=pub_date,
            )
            for title, content, author, category, _, pub_date in articles_data
        ])

        for article, (_, _, _, _, article_tags, _) in zip(articles, articles_data):
            article.tags.set(article_tags)

        articles_qs = (
            Article.objects
            .defer('content')
            .select_related('author', 'category')
            .prefetch_related('tags')
        )

        self.stdout.write("Created articles (content field deferred):")
        for article in articles_qs:
            tag_names = ", ".join(f"#{tag.name}" for tag in article.tags.all())
            self.stdout.write(
                f"  - {article.title} | {article.pub_date:%Y-%m-%d} | "
                f"{article.author.name} | {article.category.name} | {tag_names}"
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(articles)} articles"))
