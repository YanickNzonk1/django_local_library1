from django.contrib import admin

from catalog.models import Genre, Author, Book, BookInstance, Language

#Register your models here.
# admin.site.register(Book)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)


class BookInstanceInline(admin.TabularInline):
    list_display = ('book', 'status', 'due_back', 'id')
    model = BookInstance
    


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (
            None,
            {
                'fields' : ('book', 'imprint', 'id')
            }
        ), 

        (
            'Availability',
            {
                'fields' : ('status', 'due_back')
            }
        ), 

    )

class BookInline(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline,]
