from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify 


class Post(models.Model):
    title = models.CharField(_("العنوان :"), max_length=50)
    text = models.TextField(_("الوصف :"), max_length=500)
    image = models.ImageField(_("الصوره :"), upload_to='image', blank=True, null=True  )
    created_in = models.DateTimeField(_("انشاء فى :"),auto_now_add=True, blank=True, null=True)
    update_by = models.DateTimeField(_("تم التحديث :"),auto_now_add=True, blank=True, null=True)
    auther = models.ForeignKey(User , related_name='auther', on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug :"), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-created_in', )


