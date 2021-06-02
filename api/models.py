from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()


class Reviews(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.text[:15]} - {self.author} - {self.pub_date}'


class Comments(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Reviews,
        on_delete=CASCADE,
        related_name='reviews',
    )

    def __str__(self):
        return f'{self.text[:15]} - {self.author} - {self.pub_date}'
