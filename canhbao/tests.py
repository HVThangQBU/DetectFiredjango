from django.test import SimpleTestCase


class SimpleTests(SimpleTestCase):
  # def test_home_page_status(self):
  #   response = self.client.get('/')
  #   self.assertEqual(response.status_code, 200)

  def test_detail_camera_page_status(self):
    response = self.client.get('detail_camera/')
    self.assertEqual(response.status_code, 200)

# Create your tests here.
