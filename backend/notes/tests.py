from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notes.models import Note, Comment, NoteLike, CommentLike


class AuthAndUsersApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='api_user', password='pass12345')
        self.other_user = User.objects.create_user(username='api_user_2', password='pass12345')

    def test_token_auth_endpoint(self):
        response = self.client.post(
            reverse('api-token-auth'),
            {'username': 'api_user', 'password': 'pass12345'},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_users_list_and_create(self):
        self.client.force_authenticate(self.user)

        list_response = self.client.get(reverse('user-list'))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        create_response = self.client.post(
            reverse('user-list'),
            {'username': 'created_from_api', 'email': 'created@example.com'},
            format='json',
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

    def test_user_top_endpoints(self):
        note = Note.objects.create(author=self.user, title='N', content='C')
        Comment.objects.create(author=self.user, note=note, text='comment')

        response_notes = self.client.get(reverse('user-top-by-notes'))
        self.assertEqual(response_notes.status_code, status.HTTP_200_OK)

        response_comments = self.client.get(reverse('user-top-by-comments'))
        self.assertEqual(response_comments.status_code, status.HTTP_200_OK)


class NotesApiTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='note_author', password='pass12345')
        self.other = User.objects.create_user(username='note_other', password='pass12345')
        self.note = Note.objects.create(author=self.author, title='Title', content='Body')

    def test_notes_crud_and_permissions(self):
        list_response = self.client.get(reverse('note-list'))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        unauth_create = self.client.post(
            reverse('note-list'),
            {'title': 'New note', 'content': 'Text'},
            format='json',
        )
        self.assertEqual(unauth_create.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.author)
        auth_create = self.client.post(
            reverse('note-list'),
            {'title': 'New note', 'content': 'Text'},
            format='json',
        )
        self.assertEqual(auth_create.status_code, status.HTTP_201_CREATED)

        detail_response = self.client.get(reverse('note-detail', args=[self.note.id]))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

        self.client.force_authenticate(self.other)
        forbidden_update = self.client.patch(
            reverse('note-detail', args=[self.note.id]),
            {'title': 'Hack'},
            format='json',
        )
        self.assertEqual(forbidden_update.status_code, status.HTTP_403_FORBIDDEN)

    def test_note_actions(self):
        self.client.force_authenticate(self.author)

        like_response = self.client.post(reverse('note-like', args=[self.note.id]))
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertTrue(NoteLike.objects.filter(note=self.note, user=self.author).exists())

        unlike_response = self.client.post(reverse('note-unlike', args=[self.note.id]))
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)

        pin_response = self.client.post(reverse('note-pin', args=[self.note.id]))
        self.assertEqual(pin_response.status_code, status.HTTP_200_OK)

        unpin_response = self.client.post(reverse('note-unpin', args=[self.note.id]))
        self.assertEqual(unpin_response.status_code, status.HTTP_200_OK)

        my_response = self.client.get(reverse('note-my'))
        self.assertEqual(my_response.status_code, status.HTTP_200_OK)

        popular_response = self.client.get(reverse('note-popular'))
        self.assertEqual(popular_response.status_code, status.HTTP_200_OK)

        pinned_response = self.client.get(reverse('note-pinned'))
        self.assertEqual(pinned_response.status_code, status.HTTP_200_OK)

        stats_response = self.client.get(reverse('note-stats'))
        self.assertEqual(stats_response.status_code, status.HTTP_200_OK)

        lightweight_response = self.client.get(reverse('note-lightweight'))
        self.assertEqual(lightweight_response.status_code, status.HTTP_200_OK)


class CommentsApiTests(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(username='comment_author', password='pass12345')
        self.other = User.objects.create_user(username='comment_other', password='pass12345')
        self.note = Note.objects.create(author=self.author, title='Note for comments', content='Body')
        self.comment = Comment.objects.create(author=self.author, note=self.note, text='Initial comment')

    def test_comments_crud_and_filter(self):
        list_response = self.client.get(reverse('comment-list'))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        filtered_response = self.client.get(f"{reverse('comment-list')}?note={self.note.id}")
        self.assertEqual(filtered_response.status_code, status.HTTP_200_OK)

        unauth_create = self.client.post(
            reverse('comment-list'),
            {'note': self.note.id, 'text': 'No auth'},
            format='json',
        )
        self.assertEqual(unauth_create.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.author)
        auth_create = self.client.post(
            reverse('comment-list'),
            {'note': self.note.id, 'text': 'With auth'},
            format='json',
        )
        self.assertEqual(auth_create.status_code, status.HTTP_201_CREATED)

        self.client.force_authenticate(self.other)
        forbidden_update = self.client.patch(
            reverse('comment-detail', args=[self.comment.id]),
            {'text': 'Hack'},
            format='json',
        )
        self.assertEqual(forbidden_update.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_actions(self):
        self.client.force_authenticate(self.author)

        like_response = self.client.post(reverse('comment-like', args=[self.comment.id]))
        self.assertEqual(like_response.status_code, status.HTTP_200_OK)
        self.assertTrue(CommentLike.objects.filter(comment=self.comment, user=self.author).exists())

        unlike_response = self.client.post(reverse('comment-unlike', args=[self.comment.id]))
        self.assertEqual(unlike_response.status_code, status.HTTP_200_OK)

        popular_response = self.client.get(reverse('comment-popular'))
        self.assertEqual(popular_response.status_code, status.HTTP_200_OK)

        by_author_response = self.client.get(f"{reverse('comment-by-author')}?author_id={self.author.id}")
        self.assertEqual(by_author_response.status_code, status.HTTP_200_OK)

        by_author_no_param_response = self.client.get(reverse('comment-by-author'))
        self.assertEqual(by_author_no_param_response.status_code, status.HTTP_400_BAD_REQUEST)


class LikesReadOnlyApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='likes_user', password='pass12345')
        self.note = Note.objects.create(author=self.user, title='Liked note', content='Body')
        self.comment = Comment.objects.create(author=self.user, note=self.note, text='Liked comment')
        self.note_like = NoteLike.objects.create(user=self.user, note=self.note)
        self.comment_like = CommentLike.objects.create(user=self.user, comment=self.comment)

    def test_note_likes_read_only(self):
        list_response = self.client.get(reverse('notelike-list'))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        detail_response = self.client.get(reverse('notelike-detail', args=[self.note_like.id]))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    def test_comment_likes_read_only(self):
        list_response = self.client.get(reverse('commentlike-list'))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

        detail_response = self.client.get(reverse('commentlike-detail', args=[self.comment_like.id]))
        self.assertEqual(detail_response.status_code, status.HTTP_200_OK)

    def test_likes_create_not_allowed(self):
        self.client.force_authenticate(self.user)

        create_note_like = self.client.post(
            reverse('notelike-list'),
            {'note': self.note.id},
            format='json',
        )
        self.assertEqual(create_note_like.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        create_comment_like = self.client.post(
            reverse('commentlike-list'),
            {'comment': self.comment.id},
            format='json',
        )
        self.assertEqual(create_comment_like.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
