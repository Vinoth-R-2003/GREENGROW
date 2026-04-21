from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Plant, UserPlant, Harvest, GardenTask, HealthLog, GardenExpense
from datetime import date

User = get_user_model()

class GardenEnhancementTests(TestCase):
    def setUp(self):
        # Create user and log in
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = Client()
        self.client.login(username='testuser', password='password123')
        
        # Create plant
        self.plant = Plant.objects.create(
            name='Test Tomato',
            description='A red test tomato',
            how_to_grow='Easy',
            how_to_use='Salads'
        )
        
        # Create UserPlant
        self.user_plant = UserPlant.objects.create(
            user=self.user,
            plant=self.plant,
            status='Growing'
        )

    def test_harvest_creation(self):
        url = reverse('harvest_list', args=[self.user_plant.id])
        data = {
            'date': date.today(),
            'quantity': 2.5,
            'unit': 'kg',
            'rating': 5,
            'notes': 'Great harvest!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302) # Should redirect
        self.assertTrue(Harvest.objects.filter(user_plant=self.user_plant).exists())
        harvest = Harvest.objects.get(user_plant=self.user_plant)
        self.assertEqual(harvest.quantity, 2.5)

    def test_task_creation_and_completion(self):
        # Create Task
        url = reverse('task_list', args=[self.user_plant.id])
        data = {
            'task_type': 'Watering',
            'due_date': date.today(),
            'notes': 'Water deeply'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        task = GardenTask.objects.get(user_plant=self.user_plant)
        self.assertEqual(task.task_type, 'Watering')
        self.assertFalse(task.is_completed)

        # Complete Task
        complete_url = reverse('complete_task', args=[task.id])
        response = self.client.get(complete_url) # Using get as per view implementation
        self.assertEqual(response.status_code, 302)
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

    def test_health_log_creation(self):
        url = reverse('health_log_list', args=[self.user_plant.id])
        data = {
            'issue_type': 'Pest',
            'severity': 'Medium',
            'status': 'Identified',
            'notes': 'Aphids spotted'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(HealthLog.objects.filter(user_plant=self.user_plant).exists())

    def test_expense_creation(self):
        url = reverse('expense_list')
        data = {
            'item_name': 'Fertilizer',
            'cost': 15.50,
            'date': date.today(),
            'category': 'Other'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(GardenExpense.objects.filter(user=self.user).exists())
        expense = GardenExpense.objects.get(user=self.user)
        self.assertEqual(float(expense.cost), 15.50)

    def test_qr_generation(self):
        url = reverse('generate_qr_code', args=[self.user_plant.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.user_plant.refresh_from_db()
        self.assertTrue(self.user_plant.qr_code)
