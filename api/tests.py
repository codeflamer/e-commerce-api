from django.test import TestCase
from api.models import User,Order
from django.urls import reverse
from rest_framework import status

# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user1",password="user1")
        user2 = User.objects.create_user(username="user2",password="user2")
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2) 
    
    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username="user1")
        self.client.force_login(user)
        response = self.client.get(reverse('user-orders'))

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order["user"] == user.id for order in orders))

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('user-orders'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductListTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username="user4",password="user4")
        user2 = User.objects.create_superuser(username="user5",password="user5")

    def test_authenticated_user_list_create_product(self):
        ### testing normal user ####
        normal_user = User.objects.get(username="user4")
        self.client.force_login(normal_user)
        ## getting a request
        response = self.client.get(reverse("user-products"))
        self.assertTrue(response.status_code ==  status.HTTP_200_OK)
        ## posting a request
        response = self.client.post(reverse("user-products"))
        self.assertTrue(response.status_code ==  status.HTTP_403_FORBIDDEN)


        ### testing super user ####
        super_user = User.objects.get(username="user5")
        self.client.force_login(super_user)
        ## getting a request
        response = self.client.get(reverse("user-products"))
        self.assertTrue(response.status_code ==  status.HTTP_200_OK)
         ## posting a request
        response = self.client.post(reverse("user-products"))
        self.assertTrue(response.status_code ==  status.HTTP_400_BAD_REQUEST)
        ## posting a request
        response = self.client.post(reverse("user-products"),
            {
                "name":"Butter",
                "description":"An amazing butter",
                "price":"200",
                "stock":"4"
            }
        )
        self.assertTrue(response.status_code ==  status.HTTP_201_CREATED)


