from django.db import models

# Create your models here.

class contact_us(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='پیام')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال پیام')
    response = models.TextField(null=True, blank=True, verbose_name='پاسخ ادمین')
    is_read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)