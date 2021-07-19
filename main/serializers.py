from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers, fields
from rest_framework.relations import PrimaryKeyRelatedField
from main.models import Author, Book, Tag


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'books_count')


class BaseBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'pages')


class BookSerializer(BaseBookSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = fields.IntegerField(write_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'pages', 'author', 'author_id')


class ExtendedAuthorSerializer(serializers.ModelSerializer):
    books = BaseBookSerializer(many=True)

    def validate(self, attrs):
        if age := attrs['age']:
            if age < 0:
                raise ValidationError(
                    {'age': 'Age must be greater or equal to zero'}
                )
        return super().validate(attrs)

    class Meta:
        model = Author
        fields = ('id', 'name', 'age', 'books', 'books_count')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'title', 'tagged_books_count')


class TagAttacherSerializer(serializers.Serializer):
    tag_id = PrimaryKeyRelatedField(queryset=Tag.objects.all())

    def validate(self, attrs):
        if attrs['tag_id'] is None:
            raise ValidationError({'tag_id': 'This field is missing'})
        return super().validate(attrs)

    class Meta:
        fields = ('tag_id')


class ExtendedBookSerializer(BookSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'pages', 'author', 'tags')


class BookTagAttacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('tags', )

    def to_representation(self, instance):
        self.fields['tags'] = TagSerializer(many=True)
        return super().to_representation(instance)
