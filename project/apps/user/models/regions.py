from django.db import models


class Region(models.Model):
    parent_region = models.ForeignKey('self', models.CASCADE, blank=True, null=True)
    names = models.ManyToManyField('translations.Translation', blank=True)
    
    shipment_price = models.FloatField(default=0)
    minimum_order_price = models.FloatField()
    minimum_order_free_ship_price = models.FloatField()
    fixed_shipment_price = models.FloatField()

    currency_code = models.CharField(max_length=16)

    def get_order_shipment_price(self, order_price):
        shipping = self.shipment_price if order_price < (self.minimum_order_free_ship_price) else 0
        shipping = shipping + self.fixed_shipment_price
        return shipping

    def __str__(self) -> str:
        return f"{self.pk} - {self.currency_code}"