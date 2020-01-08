from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.db.models.signals import post_save
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User , verbose_name=_("user_profile"), on_delete=models.CASCADE)
    image = models.ImageField(_("الصوره : "), upload_to='user-image')
    country = CountryField(_("العنوان :"))
    address = models.CharField(max_length=50, blank=True, null=True)
    who_i = models.TextField(_("السيره الذاتيه :"), max_length=300)
    slug = models.SlugField(_("Slug :"),blank=True, null=True)

    def __str__(self):
        return '%s' %(self.user.username)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile, self).save(*args, **kwargs)


        img = Image.open(self.image.path) #If the image > "300w ,300h" this variable will minimize it using pillow library 
        if img.width > 300 or img.height > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

def create_profile(sender , **kwrag):
    if kwrag['created']:
        Profile.objects.create(user=kwrag['instance'])

post_save.connect(create_profile , sender=User)