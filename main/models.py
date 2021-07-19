from django.db import models

# Create your models here.


class HeroloUser(models.Model):
    name = models.CharField(max_length=10)
    age = models.IntegerField(blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def tagged_books_count(self):
        return self.books.count()

    def __str__(self) -> str:
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()

    def books_count(self):
        return self.books.count()

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    pages = models.PositiveIntegerField()
    author = models.ForeignKey(
        Author, related_name="books", on_delete=models.CASCADE, blank=True)
    tags = models.ManyToManyField(Tag, related_name="books")

    def __str__(self) -> str:
        return f'{self.title}" by {self.author}'
