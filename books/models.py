from django.db import models
from django.contrib.auth.models import User
from category.models import CategoryModel

# Create your models here.
class Books(models.Model):
   user=models.ForeignKey(User, related_name='user',on_delete=models.CASCADE) 
   image = models.ImageField(upload_to = 'images/')
   title = models.CharField(max_length = 200)
   prize=models.IntegerField()
   details = models.TextField(default = '')
   category=models.ManyToManyField(CategoryModel)

   def __str__(self) -> str:
      return self.title
   
class comments(models.Model):
    name = models.CharField(max_length=20)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    car_model = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='comments')
    def __str__(self):
        return self.name