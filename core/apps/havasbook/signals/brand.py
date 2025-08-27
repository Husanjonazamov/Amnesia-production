import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from core.apps.havasbook.models import BrandModel, BookModel

logger = logging.getLogger(__name__)

def update_brand_status(brand):
    """Brand uchun mahsulot borligini yangilash"""
    if not brand:
        logger.warning("Brand topilmadi!")
        return

    has_products = brand.products.exists()
    brand.has_products = has_products
    brand.save(update_fields=['has_products'])
    
    logger.info(f"[BRAND STATUS UPDATED] Brand: {brand.name} -> has_products={has_products}")

@receiver(post_save, sender=BookModel)
def product_created_or_updated(sender, instance, **kwargs):
    logger.info(f"[PRODUCT SAVED] Product: {instance.id} for Brand: {instance.brand.name}")
    update_brand_status(instance.brand)

@receiver(post_delete, sender=BookModel)
def product_deleted(sender, instance, **kwargs):
    logger.info(f"[PRODUCT DELETED] Product: {instance.id} for Brand: {instance.brand.name}")
    update_brand_status(instance.brand)

@receiver(post_save, sender=BrandModel)
def BrandSignal(sender, instance, created, **kwargs):
    action = "CREATED" if created else "UPDATED"
    logger.info(f"[BRAND {action}] Brand: {instance.name}")
