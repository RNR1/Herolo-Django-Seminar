from django.contrib import admin
from main.models import Author, Book, HeroloUser, Tag

# Register your models here.
admin.site.site_header = 'Herolo Django Seminar administration'


@admin.register(HeroloUser)
class HeroloUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'tagged_books_count')
    search_fields = ('title', )

    @admin.display(ordering='-books')
    def tagged_books_count(self, instance):
        return instance.tagged_books_count()


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'books_count')

    @admin.display(ordering="-books")
    def books_count(self, author):
        return author.books.count()


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'pages', 'author')
    autocomplete_fields = ('tags', )
