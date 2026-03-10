"""Seed script to populate the database with demo data."""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tinderhleb.settings')

sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from django.contrib.auth.models import User
from core.models import Profile, Event, Purchase
from datetime import datetime, timedelta
from django.utils import timezone

# Demo users
demo_users = [
    {
        'nickname': 'Анна',
        'card': 'TH-0001',
        'gender': 'F',
        'age': 25,
        'about': 'Обожаю выпечку и долгие прогулки. Ищу компанию для утреннего кофе с круассаном!',
        'keywords': 'кофе, книги, прогулки, выпечка, йога',
        'favorite': 'круассан, латте, чизкейк',
        'mode': 'friends',
    },
    {
        'nickname': 'Дмитрий',
        'card': 'TH-0002',
        'gender': 'M',
        'age': 28,
        'about': 'Программист, фанат свежего хлеба. Каждое утро начинаю с чиабатты.',
        'keywords': 'программирование, спорт, кофе, настолки, музыка',
        'favorite': 'чиабатта, эспрессо, багет',
        'mode': 'friends',
    },
    {
        'nickname': 'Мария',
        'card': 'TH-0003',
        'gender': 'F',
        'age': 23,
        'about': 'Студентка, обожаю пробовать новую выпечку. Ржаной с семечками — моя слабость!',
        'keywords': 'учёба, музыка, путешествия, фотография, кулинария',
        'favorite': 'ржаной с семечками, булочка с корицей, капучино',
        'mode': 'love',
    },
    {
        'nickname': 'Алексей',
        'card': 'TH-0004',
        'gender': 'M',
        'age': 30,
        'about': 'Повар-любитель, делаю лучшие сэндвичи в районе!',
        'keywords': 'кулинария, спорт, кофе, кино, путешествия',
        'favorite': 'багет, фокачча, круассан',
        'mode': 'love',
    },
    {
        'nickname': 'Катя',
        'card': 'TH-0005',
        'gender': 'F',
        'age': 27,
        'about': 'Фотограф, ищу друзей для совместных завтраков и фото-вылазок.',
        'keywords': 'фотография, искусство, кофе, прогулки, выпечка',
        'favorite': 'круассан, тирамису, латте',
        'mode': 'friends',
    },
    {
        'nickname': 'Олег',
        'card': 'TH-0006',
        'gender': 'M',
        'age': 35,
        'about': 'Архитектор. Люблю начинать день с бриоши и капучино. Всегда за новые знакомства.',
        'keywords': 'архитектура, дизайн, кофе, велосипед, кино',
        'favorite': 'бриошь, капучино, фокачча',
        'mode': 'friends',
    },
    {
        'nickname': 'Настя',
        'card': 'TH-0007',
        'gender': 'F',
        'age': 22,
        'about': 'Танцую и пеку на досуге. Мечтаю открыть свою пекарню!',
        'keywords': 'танцы, кулинария, выпечка, музыка, йога',
        'favorite': 'булочка с корицей, шоколадный маффин, латте',
        'mode': 'love',
    },
    {
        'nickname': 'Руслан',
        'card': 'TH-0008',
        'gender': 'M',
        'age': 26,
        'about': 'Бариста в душе, маркетолог по профессии. Знаю всё о сочетании кофе и хлеба.',
        'keywords': 'кофе, маркетинг, книги, бег, настолки',
        'favorite': 'чиабатта, эспрессо, тирамису',
        'mode': 'love',
    },
    {
        'nickname': 'Лиза',
        'card': 'TH-0009',
        'gender': 'F',
        'age': 29,
        'about': 'Дизайнер интерьеров. Обожаю уютные кафе, ароматный хлеб и долгие разговоры.',
        'keywords': 'дизайн, искусство, путешествия, кофе, книги',
        'favorite': 'круассан, чизкейк, раф',
        'mode': 'friends',
    },
    {
        'nickname': 'Максим',
        'card': 'TH-0010',
        'gender': 'M',
        'age': 31,
        'about': 'Учитель истории. После уроков иду за свежим багетом — традиция!',
        'keywords': 'история, книги, кино, прогулки, кулинария',
        'favorite': 'багет, ржаной с семечками, американо',
        'mode': 'friends',
    },
    {
        'nickname': 'Полина',
        'card': 'TH-0011',
        'gender': 'F',
        'age': 24,
        'about': 'Журналистка и фуд-блогер. Пишу про лучшие пекарни города.',
        'keywords': 'журналистика, фотография, кулинария, путешествия, кофе',
        'favorite': 'фокачча, круассан, капучино',
        'mode': 'love',
    },
    {
        'nickname': 'Артём',
        'card': 'TH-0012',
        'gender': 'M',
        'age': 27,
        'about': 'Музыкант, играю на гитаре в кафе по выходным. Хлеб и музыка — лучший дуэт.',
        'keywords': 'музыка, гитара, кофе, спорт, настолки',
        'favorite': 'чиабатта, булочка с корицей, латте',
        'mode': 'friends',
    },
    {
        'nickname': 'Вика',
        'card': 'TH-0013',
        'gender': 'F',
        'age': 26,
        'about': 'Ветеринар. После смены всегда захожу за тёплым хлебом — лучшая терапия!',
        'keywords': 'животные, прогулки, выпечка, йога, кино',
        'favorite': 'ржаной хлеб, шоколадный маффин, какао',
        'mode': 'friends',
    },
    {
        'nickname': 'Денис',
        'card': 'TH-0014',
        'gender': 'M',
        'age': 33,
        'about': 'Фитнес-тренер. Да, я ем хлеб, и нет, это не грех. Цельнозерновой рулит!',
        'keywords': 'спорт, фитнес, кулинария, бег, велосипед',
        'favorite': 'цельнозерновой, багет, протеиновый маффин',
        'mode': 'love',
    },
    {
        'nickname': 'Соня',
        'card': 'TH-0015',
        'gender': 'F',
        'age': 21,
        'about': 'Студентка-психолог. Верю, что хлеб объединяет людей лучше любой терапии.',
        'keywords': 'психология, книги, учёба, кофе, музыка',
        'favorite': 'круассан, латте, чизкейк',
        'mode': 'love',
    },
]

print("Creating demo users...")
for data in demo_users:
    username = f"card_{data['card']}"
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(username=username, password='demo1234')
        Profile.objects.create(
            user=user,
            nickname=data['nickname'],
            card_number=data['card'],
            gender=data['gender'],
            age=data['age'],
            about=data['about'],
            keywords=data['keywords'],
            favorite_item=data['favorite'],
            search_mode=data['mode'],
            bonuses=150 + int(data['card'][-1]) * 50,
        )
        # Add some purchases
        items = [
            ('Чиабатта', 180, 18),
            ('Круассан с миндалём', 220, 22),
            ('Латте', 280, 28),
            ('Ржаной хлеб', 150, 15),
            ('Булочка с корицей', 170, 17),
        ]
        for i, (item, price, bonus) in enumerate(items[:3]):
            Purchase.objects.create(
                user=user,
                item_name=item,
                price=price,
                bonuses_earned=bonus,
            )
        print(f"  Created: {data['nickname']} ({data['card']})")

# Events
print("Creating events...")
now = timezone.now()
events_data = [
    ('Дегустация новых круассанов', 'Приходите попробовать 5 новых вкусов круассанов от нашего пекаря!', now + timedelta(days=3), 30),
    ('Мастер-класс по выпечке хлеба', 'Научитесь печь настоящий ремесленный хлеб вместе с нами.', now + timedelta(days=7), 15),
    ('Утренний кофе-нетворкинг', 'Знакомьтесь с соседями за чашкой кофе и свежей выпечкой.', now + timedelta(days=10), 25),
    ('Хлебный фестиваль', 'Большой праздник с дегустациями, мастер-классами и живой музыкой!', now + timedelta(days=14), 100),
]

for title, desc, date, max_p in events_data:
    if not Event.objects.filter(title=title).exists():
        Event.objects.create(title=title, description=desc, date=date, max_participants=max_p)
        print(f"  Created event: {title}")

print("\nDone! You can log in with any card number (TH-0001 to TH-0015) and password: demo1234")
