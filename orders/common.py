from enum import Enum

class OrderStatus(Enum):
    CREATED = 'CREATED'
    PAYED = 'PAYED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'
# Create your models here.

choices = [(tag, tag.value) for tag in OrderStatus ]
