from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class ContactUs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    message = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = 'contact us'

    def short_message(self):
        return self.message[:25]

    def __str__(self):
        return f'{self.user}: {self.message}'
