from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_mock_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Note = apps.get_model('notes', 'Note')
    Comment = apps.get_model('notes', 'Comment')
    NoteLike = apps.get_model('notes', 'NoteLike')
    CommentLike = apps.get_model('notes', 'CommentLike')

    pwd = make_password('password123')
    users = [
        User.objects.create(username='admin', email='admin@example.com',
                            password=make_password('admin123'), is_staff=True, is_superuser=True),
        User.objects.create(username='ivan_ivanov', email='ivan@example.com',
                            password=pwd, first_name='Иван', last_name='Иванов'),
        User.objects.create(username='maria_petrova', email='maria@example.com',
                            password=pwd, first_name='Мария', last_name='Петрова'),
        User.objects.create(username='alex_smirnov', email='alex@example.com',
                            password=pwd, first_name='Александр', last_name='Смирнов'),
    ]

    notes = [
        Note.objects.create(author=users[0], title='Добро пожаловать в Notes API',
            content='Это первая заметка. Создавайте и делитесь заметками.', is_pinned=True, likes_count=5),
        Note.objects.create(author=users[1], title='Список дел на неделю',
            content='1. Проект по Python\n2. Спортзал\n3. Продукты\n4. Позвонить родителям', likes_count=3),
        Note.objects.create(author=users[1], title='Рецепт борща',
            content='Свекла, капуста, картофель, морковь, лук, томатная паста, бульон. Варить 2 часа.', likes_count=8),
        Note.objects.create(author=users[2], title='Идеи для путешествий',
            content='Байкал летом, Карелия осенью, Алтай весной, Кавказ зимой', is_pinned=True, likes_count=12),
        Note.objects.create(author=users[2], title='Книги к прочтению',
            content='Мастер и Маргарита, 1984, Преступление и наказание', likes_count=6),
        Note.objects.create(author=users[3], title='Заметки по программированию',
            content='Python: list comprehension. Django: select_related для оптимизации запросов.', likes_count=15),
        Note.objects.create(author=users[3], title='Мотивация на день',
            content='Каждый день - новая возможность стать лучше!', likes_count=4),
    ]

    comments = [
        Comment.objects.create(author=users[1], note=notes[0], text='Отличная заметка!', likes_count=2),
        Comment.objects.create(author=users[2], note=notes[0], text='Буду пользоваться!', likes_count=3),
        Comment.objects.create(author=users[3], note=notes[1], text='Добавь выучить фреймворк', likes_count=1),
        Comment.objects.create(author=users[0], note=notes[2], text='Обожаю борщ! Добавьте сметану!', likes_count=5),
        Comment.objects.create(author=users[2], note=notes[2], text='Добавляю фасоль, очень вкусно', likes_count=2),
        Comment.objects.create(author=users[1], note=notes[3], text='Байкал - невероятное место!', likes_count=4),
        Comment.objects.create(author=users[3], note=notes[5], text='Полезные советы!', likes_count=3),
        Comment.objects.create(author=users[0], note=notes[5], text='Ещё рекомендую prefetch_related', likes_count=6),
    ]

    for u, n in [(0,3),(1,3),(2,3),(0,5),(1,5),(2,2),(3,2),(1,0),(2,0)]:
        NoteLike.objects.create(user=users[u], note=notes[n])

    for u, c in [(0,3),(1,3),(0,7),(2,1),(3,5)]:
        CommentLike.objects.create(user=users[u], comment=comments[c])


def delete_mock_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Note = apps.get_model('notes', 'Note')
    Comment = apps.get_model('notes', 'Comment')
    NoteLike = apps.get_model('notes', 'NoteLike')
    CommentLike = apps.get_model('notes', 'CommentLike')

    CommentLike.objects.all().delete()
    NoteLike.objects.all().delete()
    Comment.objects.all().delete()
    Note.objects.all().delete()
    User.objects.filter(username__in=['admin', 'ivan_ivanov', 'maria_petrova', 'alex_smirnov']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_mock_data, delete_mock_data),
    ]
