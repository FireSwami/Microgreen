from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from green.models import Green, Category
from cart.models import OrderLineItem, OrderLineItem

User = get_user_model()

class ShopTestCases(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(username='testuser', password='password')
        self.category = Category.objects.create(name='Микрозелень', slug='microgreen')
        # image = SimpleUploaderFile('image.jpg', content=b'', content_type='image/jpg')
        self.green = Green.objects.create(
            title = "Test_microgreen",
            slug = 'Test_slug',
            photo = 'image',
            cat = self.category,
            price = Decimal('30.00'),
        
        )
