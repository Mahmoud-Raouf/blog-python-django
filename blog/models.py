from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify 


class Post(models.Model):
    title = models.CharField(_("العنوان :"), max_length=50)
    short_description = models.TextField(_("وصف صغير :"), max_length=100)
    description = models.TextField(_("الوصف :"), max_length=500)
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



class Comment(models.Model):
    name = models.CharField(_("الاسم:"), max_length=50)
    email = models.EmailField(_("الايميل :"), max_length=50)
    coment = models.TextField(_("التعليق :"), max_length=500)
    coment_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(_("الحاله :"), default=False)
    post = models.ForeignKey(Post , related_name='comments', on_delete=models.CASCADE)


    def __str__(self):
        return '{} علق على {}'.format(self.name , self.post)

    class Meta:
        ordering = ('-coment_date',)