# """
# Проверяет доступ к страницам сайта. Требует поднятие сервера. Потому под коментарием.
# """
# import unittest
#
# import requests
# from django.views.decorators.csrf import csrf_exempt
#
# url = "http://127.0.0.1:8000/login/"
# data = {
#     "username": "test",
#     "password": "Testpassword1"
# }
#
# class TestCode(unittest.TestCase):
#     @csrf_exempt
#     def test_code(self):
#         response = requests.request("GET", "http://127.0.0.1:8000")
#         self.assertTrue(response.status_code, 200)
#
#         response = requests.request("GET", "http://127.0.0.1:8000/contact/")
#         self.assertTrue(response.status_code, 200)
#
#         response = requests.request("GET", "http://127.0.0.1:8000/about/")
#         self.assertTrue(response.status_code, 200)
#
#         response = requests.request("GET", "http://127.0.0.1:8000/cart/")
#         self.assertTrue(response.status_code, 200)
#
#         response = requests.request("POST", url, data=data)
#         self.assertTrue(response.status_code, 200)
#
#         response = requests.request("GET", "http://127.0.0.1:8000/category/microgreen/")
#         self.assertTrue(response.status_code, 200)
