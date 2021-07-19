from rest_framework import viewsets
from rest_framework.decorators import action
from django.http import JsonResponse
from main.models import Author, Book, Tag
from main.serializers import AuthorSerializer, BookSerializer, BookTagAttacherSerializer, ExtendedAuthorSerializer, ExtendedBookSerializer, TagAttacherSerializer, TagSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_serializer_class(self):
        if self.action != 'list':
            return ExtendedAuthorSerializer
        return AuthorSerializer

    class Meta:
        model = Author


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ExtendedBookSerializer
        return BookSerializer

    @action(methods=('patch', ), detail=True)
    def add_tag(self, request, pk):
        instance = self.get_object()
        tag_serializer = TagAttacherSerializer(data=request.data)
        tag_serializer.is_valid(raise_exception=True)
        updated_tags = list(instance.tags.values_list('id', flat=True))
        updated_tags.append(tag_serializer.validated_data['tag_id'].id)
        instance.tags.set(updated_tags)
        book_serializer = BookTagAttacherSerializer(
            instance, data={'tags': updated_tags})
        book_serializer.is_valid(raise_exception=True)
        book_serializer.save()
        return JsonResponse(book_serializer.data)

    class Meta:
        model = Book


class TagViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'delete']
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    class Meta:
        model = Tag
