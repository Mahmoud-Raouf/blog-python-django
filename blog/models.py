from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify 
from django.urls import reverse #To tell PostCreateView what url to redirect it

class Post(models.Model):
    title = models.CharField(_("العنوان :"), max_length=50)
    short_description = models.TextField(_("وصف صغير :"), max_length=100)
    description = models.TextField(_("الوصف :"), max_length=500)
    image = models.ImageField(_("الصوره :"), upload_to='image', blank=True, null=True  )
    created_in = models.DateTimeField(_("انشاء فى :"),auto_now_add=True, blank=True, null=True)
    update_by = models.DateTimeField(_("تم التحديث :"),auto_now_add=True, blank=True, null=True)
    author = models.ForeignKey(User , related_name='author', on_delete=models.CASCADE)
    slug = models.SlugField(_("Slug :"), blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', args={self.slug}) #detail+pk url
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ('-created_in', )



class Comment(models.Model):
    name = models.CharField(_("الاسم : "), max_length=50)
    email = models.EmailField(_("الايميل : "), max_length=50)
    comment = models.TextField(_("التعليق : "), max_length=500)
    comment_date = models.DateTimeField(auto_now_add=True)
    site = models.CharField(_("الموقع : "), max_length=50)
    active = models.BooleanField(_("الحاله : "), default=False, blank=True, null=True)
    post = models.ForeignKey('Post' , related_name='comments', on_delete=models.CASCADE)


    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return '{} علق على {}'.format(self.name, self.post )

    class Meta:
        ordering = ('-comment_date',)