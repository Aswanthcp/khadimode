from tabnanny import verbose

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Category(MPTTModel):
    category_name = models.CharField(
        verbose_name=_("Category Name"),
        help_text=_("Required and unique"), max_length=50, unique=True)
    discription = models.TextField(max_length=200, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories')
    offer = models.PositiveIntegerField(default=0)
    slug = models.SlugField(verbose_name=_(
        "Category safe URL"), max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE,
                            null=True, blank=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ["category_name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_url(self):
        return reverse('store:products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
