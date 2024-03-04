from django.test import TestCase
from .models import Post, Comment
from .views import PostDetail
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import render



class TestDjango(TestCase):

    def test_this_thing_works(self):
        self.assertEqual(1, 1)


class TestViews(TestCase):

    def test_posts_lists(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)