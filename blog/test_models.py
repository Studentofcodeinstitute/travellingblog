from django.test import TestCase
from .models import Post, Comment

class TestModels(TestCase):

    def test_done_defaults_to_false(self):
        post = Post.objects.create(name='Test Post')
        self.assertFalse(post.done)
    
    def test_item_string_method_returns_name(self):
        post = Post.objects.create(name='Test Post')
        self.assertEqual(str(post), 'Test Post')




