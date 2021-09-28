from .factories import *
from django.test import override_settings
import shutil
from ..views import *

TEST_DIR = 'test_data'


class TestHomeView(TestCase):

  def test_homeview_get_no_homepage_promotional(self):
    response = self.client.get(reverse('home'))
    self.assertEqual(response.status_code, 200)
    self.assertIn('No new products', str(response.content))

  def test_homeview_get_homepage_promotinal(self):
    promotional_data = HomepagePromotionalFactory()
    response = self.client.get(reverse('home'), {'promotional_data': promotional_data})
    self.assertEqual(response.status_code, 200)
    self.assertIn(promotional_data.text, str(response.content))
    self.assertIn(str(promotional_data.image.url), str(response.content))


class TestProductsView(TestCase):

  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  def test_get_no_products(self):
    response = self.client.get(reverse('products_page'))
    self.assertEqual(response.status_code, 200)
    self.assertIn('No products exist', str(response.content))

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_one_product(self):
    product = ProductFactory()
    response = self.client.get(reverse('products_page'), {'product': product})
    self.assertEqual(response.status_code, 200)
    self.assertIn(product.name, str(response.content))

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_two_products(self):
    product1 = ProductFactory()
    product2 = ProductFactory()
    response = self.client.get(reverse('products_page'), {'product': [product1, product2]})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Product.objects.all().count(), 2)
    self.assertIn(product1.image.url, str(response.content))
    self.assertIn(product2.image.url, str(response.content))


class TestProductDetailView(TestCase):

  def test_get_no_product(self):
    pk = 2
    response = self.client.get(reverse('product_detail', kwargs={'pk': pk}))
    self.assertEqual(response.status_code, 404)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_product(self):
    product = ProductFactory()
    response = self.client.get(reverse('product_detail', kwargs={'pk': product.pk}))
    self.assertEqual(response.status_code, 200)
    self.assertIn(product.image.url, str(response.content))
    self.assertIn(product.name, str(response.content))

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_post_product(self):
    size = SizesFactory()
    response = self.client.post(reverse('product_detail', kwargs={'pk': size.product.pk}),
                                {'quantity': 1, 'size': size.size_type})

    self.assertEqual(response.status_code, 200)
    self.assertIn(size.product.image.url, str(response.content))
    self.assertIn(size.product.name, str(response.content))


class TestCategoryView(TestCase):

  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_one_product(self):

    product1 = ProductFactory()
    response = self.client.get(reverse('category_view', kwargs={'name': product1.category.name}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Product.objects.all().count(), 1)
    self.assertIn(product1.image.url, str(response.content))

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_two_products(self):
    category = CategoryFactory()
    product1 = ProductFactory(category=category)
    product2 = ProductFactory(category=category)
    response = self.client.get(reverse('category_view', kwargs={'name': str(category.name)}))
    self.assertEqual(response.status_code, 200)
    self.assertEqual(Product.objects.all().count(), 2)
    self.assertIn(product1.image.url, str(response.content))
    self.assertIn(product2.image.url, str(response.content))

  def test_no_products(self):
    category = 'no_products_with_this_category'
    response = self.client.get(reverse('category_view', kwargs={'name': category}))
    self.assertEqual(response.status_code, 404)


class TestGetJson(TestCase):

  def tearDown(self):
    print("\nDeleting temporary files...\n")
    try:
      shutil.rmtree(TEST_DIR)
    except OSError:
      print(OSError)

  @override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
  def test_get_existing_size(self):
    size = SizesFactory()
    request = RequestFactory()
    response = get_json_model_data(request=request, size_pk=size.pk)
    self.assertIn(str(size.size_type[0]), str(response.content))
    self.assertIn(str(size.price), str(response.content))
    self.assertIn(str(size.quantity), str(response.content))
    self.assertIn(str(size.product.pk), str(response.content))

  def test_get_not_existing_size(self):
    request = RequestFactory()
    response = get_json_model_data(request=request, size_pk=1)
    self.assertEqual(str(response.content), 'b\'{"data": []}\'')
