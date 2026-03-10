from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]
    SEARCH_MODE_CHOICES = [
        ('friends', 'Разделить фильтр'),
        ('love', 'Купить хлеб домой'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField('Имя / Псевдоним', max_length=100)
    card_number = models.CharField('Номер клубной карты', max_length=20, unique=True)
    avatar = models.ImageField('Фото', upload_to='avatars/', blank=True, null=True)
    gender = models.CharField('Пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField('Дата рождения', blank=True, null=True)
    age = models.PositiveIntegerField('Возраст', blank=True, null=True)
    about = models.TextField('Расскажи о себе', blank=True)
    keywords = models.CharField('Ключевые слова (через запятую)', max_length=500, blank=True)
    favorite_item = models.CharField('Любимая позиция (через запятую)', max_length=300, blank=True)
    search_mode = models.CharField('Кого ищу', max_length=10, choices=SEARCH_MODE_CHOICES, blank=True)
    looking_for_gender = models.CharField('Ищу пол', max_length=1, choices=GENDER_CHOICES, blank=True)
    bonuses = models.PositiveIntegerField('Бонусы', default=150)

    def __str__(self):
        return self.nickname

    def get_keywords_list(self):
        if self.keywords:
            return [k.strip().lower() for k in self.keywords.split(',') if k.strip()]
        return []

    def get_favorite_items_list(self):
        if self.favorite_item:
            return [k.strip().lower() for k in self.favorite_item.split(',') if k.strip()]
        return []


class Match(models.Model):
    STATUS_CHOICES = [
        ('liked', 'Лайк'),
        ('disliked', 'Дизлайк'),
    ]
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}: {self.status}"


class Feedback(models.Model):
    TYPE_CHOICES = [
        ('complaint', 'Жалоба'),
        ('praise', 'Похвала'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField('Тип', max_length=10, choices=TYPE_CHOICES)
    text = models.TextField('Текст')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_feedback_type_display()} от {self.user}"


class Event(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    date = models.DateTimeField('Дата и время')
    image = models.ImageField('Изображение', upload_to='events/', blank=True, null=True)
    max_participants = models.PositiveIntegerField('Макс. участников', default=50)
    participants = models.ManyToManyField(User, related_name='events_joined', blank=True)

    def __str__(self):
        return self.title

    def spots_left(self):
        return self.max_participants - self.participants.count()


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    item_name = models.CharField('Товар', max_length=200)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    bonuses_earned = models.PositiveIntegerField('Бонусов начислено', default=0)
    date = models.DateTimeField('Дата покупки', auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} — {self.price}₽"
