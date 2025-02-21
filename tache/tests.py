from datetime import datetime, timedelta
from .models import Task, TaskCompletion, Project
from django.test import TestCase
from django.contrib.auth.models import User
class StatisticsTest(TestCase):
    def setUp(self):
        # Créer des utilisateurs, tâches et assignations
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            name='Test Task',
            description='Description de la tâche',
            due_date=datetime.today() + timedelta(days=10),
            assigned_to=self.user,
            project=self.project 
        )
        TaskCompletion.objects.create(
            user=self.user,
            task=self.task,
            completion_date=datetime.today(),
            is_completed_on_time=True
        )

    def test_statistics(self):
        response = self.client.get('/tache/statistics/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Statistiques des Tâches')
