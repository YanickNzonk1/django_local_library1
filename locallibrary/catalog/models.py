import uuid
from django.db import models


from django.urls import reverse
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower


# Create your models here.


class Genre(models.Model):
    """Model representing a book genre"""
    name=models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc.)"

    )

    def __str__(self):
        """String for representing the model object"""
        return self.name
    

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance"""
        return reverse('genre-detail', args=[str(self.id)])
    

    class Meta:
        constraints=[
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message='Genre already exists (case insensitive match)'
            ),
        ]



class Book(models.Model):
    """Model representing a book (not a specific copy of a book)"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    summary = models.TextField(max_length = 1000,
        help_text = 'Enter a brief description of the book',
    )

    isbn = models.CharField('ISBN', max_length=13, unique=True),

    genre = models.ManyToManyField('Genre', help_text='select a genre for this book')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the model object"""
        return self.title
    
    def get_absolute_url(self):
        """Return a URL to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'
        

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)"""
    id = models.UUIDField(
        primary_key = True, 
        default = uuid.uuid4,
        help_text = 'Unique ID for this particular book across whole library'
    )

    book = models.ForeignKey(
        'Book', 
        on_delete=models.RESTRICT, null=True
    )

    imprint = models.CharField(max_length=200)

    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'), 
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True, 
        default='m',
        help_text='book availability',
    )

    class Meta:
        ordering = ['due_back']
    

    def __str__(self):
        """String for representing the model object"""
        return f'{self.id} ({self.book.title})'


class Author(models.Model):
    """Model representing an author"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death  = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']


    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])
    

    def __str__(self):
        """String for representing the model object"""
        return f'{self.last_name} {self.first_name}'
    

    

class Language(models.Model):
    """Model representing a language (e.g. English, French, Japenese, etc.)"""

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter the book natural language (e.g. French, English, Japenese, etc.)"
    )

    def get_absolute_url(self):
        "Returns the url to access a particular language instance"
        return reverse("language-detail", args=[str(self.id)])
    


    def __str__(self):
        "String for representing the model object (in Admin site etc.)"
        return self.name
    

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'), 
                name = 'language_name_case_insensitive_unique',
                violation_error_message='Language already exists (case insensitive match)'
            ),
        ]

    