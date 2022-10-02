from django.db import models
from django.utils import timezone

# Create your models here.


class CreateUpdate(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.created_date:
            self.created_date = timezone.now()
        self.update_date = timezone.now()
        super().save(*args, **kwargs)
    
    class Meta:
        abstract = True
        
class Product(CreateUpdate):
    class ProductStatus(models.TextChoices):
        PUBLISH = 'PUBLISH', "PUBLISH"
        PENDING = 'PENDING', "PENDING"
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    status = models.CharField(
        max_length=15,
        choices=ProductStatus.choices,
        default=ProductStatus.PENDING
    )
    
    class Meta:
        db_table = 'product'