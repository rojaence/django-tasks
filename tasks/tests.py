from django.test import TestCase
from .models import User, Task
from django.urls import reverse


def create_user(username, password):
    return User.objects.create_user(username=username, password=password)


class TestTaskView(TestCase):
    def testUserLoguedCanSeeTasks(self):
        """ 
          Task View show the tasks were created by a user logued
        """
        user = create_user(username='ronny', password='12345')
        login = self.client.login(username='ronny', password='12345')
        task = Task.objects.create(
            title="Task 1", description="Desription task 1", important=False, user=user)
        task2 = Task.objects.create(
            title="Task 2", description="Desription task 2", important=False, user=user)
        task3 = Task.objects.create(
            title="Task 3", description="Desription task 3", important=False, user=user)
        url = reverse('tasks')
        response = self.client.get(url)
        self.assertContains(response, task.title)
        self.assertContains(response, task2.title)
        self.assertContains(response, task3.title)

    def testTasksCompletedFilter(self):
        """
          Task view show tasks by completed filter
        """
        user = create_user(username='ronny', password='12345')
        login = self.client.login(username='ronny', password='12345')
        task1 = Task.objects.create(
            title="Task 1", description="Desription task 1", important=False, user=user)
        task2 = Task.objects.create(
            title="Task 2", description="Desription task 2", important=False, user=user)
        task3 = Task.objects.create(
            title="Task 3", description="Desription task 3", important=True, user=user)
        task4 = Task.objects.create(
            title="Task 4", description="Desription task 4", important=False, user=user)

        url = reverse('tasks')
        response = self.client.get(url)
        # All tasks
        self.assertQuerysetEqual(list(response.context["tasks"]), [
                                 task1, task2, task3, task4])
        self.assertEqual(response.context["completed_filter"], '')

        # Completed tasks
        task1.completed = True
        task3.completed = True
        task1.save()
        task3.save()
        url = reverse("tasks")
        url += "?completed=true"
        response = self.client.get(url)
        self.assertContains(response, task1.title)
        self.assertContains(response, task3.title)
        self.assertEqual(response.context["completed_filter"], 'true')

        # Pending tasks
        url = reverse("tasks")
        url += "?completed=false"
        response = self.client.get(url)
        self.assertContains(response, task2.title)
        self.assertContains(response, task4.title)
        self.assertEqual(response.context["completed_filter"], 'false')
