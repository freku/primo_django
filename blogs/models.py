from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django_summernote.fields import SummernoteTextFormField, SummernoteTextField

class SlugBySaveModel(models.Model):
    sluggy_field = ''

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if  self.slug is not f"{self.pk}-{slugify(getattr(self, self.sluggy_field))}":
            self.slug = f"{self.pk}-{slugify(getattr(self, self.sluggy_field))}"
            super().save(*args, **kwargs)
    
    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class Blog(SlugBySaveModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, unique=True)
    description = models.TextField(max_length=2048)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True)
    sluggy_field = 'name'

    def __str__(self):
        return self.name

    def is_owner(self, user):
        return self.creator.pk is user.pk

    #add sorting?

class Tag(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class Post(SlugBySaveModel):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=42)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(blank=True)
    sluggy_field = 'title'

    def __str__(self):
        return self.title

    def is_owner(self, user):
        return self.blog.creator.pk is user.pk