from django.db import models
from django.contrib.auth.models import User
    
class Item(models.Model):
    RARITY_CHOICES = [
        ('common', 'Common'),
        ('uncommon', 'Uncommon'),
        ('rare', 'Rare'),
        ('epic', 'Epic'),
        ('legendary', 'Legendary'),
    ]
    durability = models.IntegerField(default=100)
    rarity = models.CharField(max_length=10, choices=RARITY_CHOICES, default='common')
    name = models.CharField(max_length=100)
    description = models.TextField()
    armor = models.IntegerField(default=0)
    power = models.IntegerField(default=0)
    hp = models.IntegerField(default=0)
    stamina = models.IntegerField(default=5)
    price = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    
class Character(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    experience = models.IntegerField(default=0)
    money = models.IntegerField(default=100)
    hp = models.IntegerField(default=10)
    default_hp = models.IntegerField(default=10)
    armor = models.IntegerField(default=1)
    power = models.IntegerField(default=5)
    items = models.ManyToManyField(Item, blank=True) 
    stamina = models.IntegerField(default=10)

    def __str__(self):
        return self.name
    
    def sell_item(self, item):
        if item in self.items.all():
            self.money += item.price // 2
            self.items.remove(item)
            self.save()

    def level_up(self):
        if self.experience >= self.level * 10:
            self.level += 1
            self.hp += 2
            self.power += 1
            self.armor += 1
            self.experience = 0 #Reset experience after leveling up (not implemented yet)
            self.save()

class Monster(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    experience_worth = models.IntegerField(default=0)
    hp = models.IntegerField(default=10)
    default_hp = models.IntegerField(default=10)
    armor = models.IntegerField(default=1)
    power = models.IntegerField(default=5)
    stamina = models.IntegerField(default=5)

    def __str__(self):
        return self.name