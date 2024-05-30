from django.test import TestCase
from django.urls import reverse
from education_content.models import Material, Chapter
from tests.models import Test, Question, Answers, QuestionType, CompletedTest, CompletedQuestion
from tests.services import is_correct_answer
from tests.views import TestRunView
from users.models import User


class TestViewsTestCase(TestCase):
    def setUp(self):
        # Create a superuser for testing
        self.user = User.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.client.login(email='admin@example.com', password='adminpass')

        # Create a Chapter for testing
        self.chapter = Chapter.objects.create(title='Test Chapter', description='Test Chapter')

        # Create a Material for testing
        self.material = Material.objects.create(topic='Test Material', text='Test Material', chapter=self.chapter)

        # Create a Test for testing
        self.test = Test.objects.create(
            title='Test Test',
            description='Test Description',
            material=self.material,
            owner=self.user
        )

    def test_change_published_status(self):
        url = reverse('tests:change_published_status', kwargs={'model': 'Test', 'pk': self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.test.refresh_from_db()
        self.assertTrue(self.test.is_published)

    def test_change_published_requested_status(self):
        url = reverse('tests:change_published_requested_status', kwargs={'model': 'Test', 'pk': self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.test.refresh_from_db()
        self.assertTrue(self.test.is_published_requested)

    def test_test_create_view(self):
        url = reverse('tests:test_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_test_update_view(self):
        url = reverse('tests:test_edit', kwargs={'pk': self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_test_list_view(self):
        url = reverse('tests:test_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_test_detail_view(self):
        url = reverse('tests:test_view', kwargs={'pk': self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_test_delete_view(self):
        url = reverse('tests:test_delete', kwargs={'pk': self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_test_run_view(self):
        url = reverse('tests:test_run', kwargs={'test_pk': self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestRunViewTestCase(TestCase):
    def setUp(self):
        # Create a superuser for testing
        self.user = User.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.client.login(email='admin@example.com', password='adminpass')

        # Create a Chapter for testing
        self.chapter = Chapter.objects.create(title='Test Chapter', description='Test Chapter')

        # Create a Material for testing
        self.material = Material.objects.create(topic='Test Material', text='Test Material', chapter=self.chapter)

        # Create a Test for testing
        self.test = Test.objects.create(
            title='Test Test',
            description='Test Description',
            material=self.material,
            owner=self.user
        )

        # Create a test QuestionType with Answers
        self.question_type = QuestionType.objects.create(title='chapter')

        # Create a test Question with Answers
        self.question = Question.objects.create(text="What is 2 + 2?", test=self.test, type=self.question_type)
        self.correct_answer = Answers.objects.create(text="4", is_correct=True, question=self.question)
        self.wrong_answer = Answers.objects.create(text="5", is_correct=False, question=self.question)

        self.test.question_set.add(self.question)

    def test_test_run_view(self):
        url = reverse('tests:test_run', kwargs={'test_pk': self.test.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_valid_answers(self):
        url = reverse('tests:test_run', kwargs={'test_pk': self.test.pk})
        data = {
            f'Question:{self.question.pk}': '4'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful submission

        # Check if CompletedTest and CompletedQuestion objects are created
        completed_test = CompletedTest.objects.get(test=self.test, user=self.user)
        self.assertIsNotNone(completed_test)
        completed_question = CompletedQuestion.objects.get(completed_test=completed_test, question=self.question)
        self.assertIsNotNone(completed_question)
        self.assertTrue(completed_question.is_correct)
        self.assertEqual(str(completed_question), completed_question.answer)

    def test_post_invalid_answers(self):
        url = reverse('tests:test_run', kwargs={'test_pk': self.test.pk})
        data = {
            f'question:{self.question.pk}': '5'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after submission

        # Check if CompletedTest and CompletedQuestion objects are created
        completed_test = CompletedTest.objects.get(test=self.test, user=self.user)
        self.assertIsNotNone(completed_test)
        completed_question = CompletedQuestion.objects.get(completed_test=completed_test, question=self.question)
        self.assertIsNotNone(completed_question)
        self.assertFalse(completed_question.is_correct)

    def test_post_multiple_correct_answers(self):
        # Create a question with multiple correct answers
        self.question3 = Question.objects.create(text="numbers?", test=self.test,
                                                 type=self.question_type)
        Answers.objects.create(text="3", is_correct=True, question=self.question3)
        Answers.objects.create(text="8", is_correct=True, question=self.question3)
        self.test.question_set.add(self.question3)

        url = reverse('tests:test_run', kwargs={'test_pk': self.test.pk})
        data = {
            f'question:{self.question3.pk}': ['3', '8']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after submission

        # Check if CompletedTest and CompletedQuestion objects are created
        completed_test = CompletedTest.objects.get(test=self.test, user=self.user)
        self.assertIsNotNone(completed_test)
        completed_question = CompletedQuestion.objects.get(completed_test=completed_test, question=self.question3)
        self.assertIsNotNone(completed_question)
        self.assertTrue(completed_question.is_correct)

    def test_post_missing_answers(self):
        url = reverse('tests:test_run', kwargs={'test_pk': self.test.pk})
        data = {}  # No answers provided
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Should stay on the same page

    def test_post_extra_answers(self):
        # Create a question with multiple correct answers
        self.question2 = Question.objects.create(text="Which are even numbers?", test=self.test,
                                                 type=self.question_type)
        Answers.objects.create(text="2", is_correct=True, question=self.question2)
        Answers.objects.create(text="4", is_correct=True, question=self.question2)
        self.test.question_set.add(self.question2)

        url = reverse('tests:test_run', kwargs={'test_pk': self.test.pk})
        data = {
            f'Question:{self.question.pk}': '4',
            f'Question:{self.question2.pk}': ['4', '2']
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after submission

        # Check if CompletedTest and CompletedQuestion objects are created
        completed_test = CompletedTest.objects.get(test=self.test, user=self.user)
        self.assertIsNotNone(completed_test)
        completed_question = CompletedQuestion.objects.get(completed_test=completed_test, question=self.question)
        self.assertIsNotNone(completed_question)
        self.assertTrue(completed_question.is_correct)

    def test_get_context_data(self):
        view = TestRunView()
        view.kwargs = {'test_pk': self.test.pk}
        context = view.get_context_data()
        self.assertEqual(context['test'], self.test)
        self.assertIn(self.question, context['question_list'])


class IsCorrectAnswerTestCase(TestCase):
    def setUp(self):
        # Create a Chapter for testing
        self.chapter = Chapter.objects.create(title='Test Chapter', description='Test Chapter')
        # Create a Material for testing
        self.material = Material.objects.create(topic='Test Material', text='Test Material', chapter=self.chapter)
        # Create a Test for testing
        self.test = Test.objects.create(title="Test", material=self.material)
        # Create a test QuestionType with Answers
        self.question_type = QuestionType.objects.create(title='Test Type')
        # Create a test Question with Answers
        self.question = Question.objects.create(text="What is 2 + 2?", test=self.test, type=self.question_type)
        self.correct_answer = Answers.objects.create(text="4", is_correct=True, question=self.question)
        self.wrong_answer = Answers.objects.create(text="5", is_correct=False, question=self.question)

    def test_correct_answer(self):
        answer_list = ["4"]
        result = is_correct_answer(self.question.pk, answer_list)
        self.assertTrue(result)

    def test_wrong_answer(self):
        answer_list = ["5"]
        result = is_correct_answer(self.question.pk, answer_list)
        self.assertFalse(result)

    def test_multiple_correct_answers(self):
        # Create a question with multiple correct answers
        self.question2 = Question.objects.create(text="Which are even numbers?", test=self.test,
                                                 type=self.question_type)
        Answers.objects.create(text="2", is_correct=True, question=self.question2)
        Answers.objects.create(text="4", is_correct=True, question=self.question2)
        Answers.objects.create(text="5", is_correct=False, question=self.question2)

        # Test with multiple correct answers
        answer_list = ["4", "2"]
        result = is_correct_answer(self.question2.pk, answer_list)
        self.assertTrue(result)

    def test_missing_correct_answer(self):
        answer_list = ["5"]
        result = is_correct_answer(self.question.pk, answer_list)
        self.assertFalse(result)

    def test_extra_correct_answer(self):
        answer_list = ["4", "5"]
        result = is_correct_answer(self.question.pk, answer_list)
        self.assertFalse(result)


class QuestionsViewTest(TestCase):

    def setUp(self):
        # Create a superuser for testing
        self.user = User.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.client.login(email='admin@example.com', password='adminpass')

        # Create a Chapter for testing
        self.chapter = Chapter.objects.create(title='Test Chapter', description='Test Chapter')

        # Create a Material for testing
        self.material = Material.objects.create(topic='Test Material', text='Test Material', chapter=self.chapter)

        # Create a Test for testing
        self.test = Test.objects.create(
            title='Test Test',
            description='Test Description',
            material=self.material,
            owner=self.user
        )

        # Create a test QuestionType with Answers
        self.question_type = QuestionType.objects.create(title='normal')

    def test_question_create_view(self):
        test_pk = self.test.pk
        response = self.client.get(reverse('tests:question_create', kwargs={'test_pk': test_pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/question_form.html')

    def test_question_create_post(self):
        test_pk = self.test.pk
        data = {'text': 'Test Question Text', 'test': test_pk, 'type': self.question_type.pk}
        response = self.client.post(reverse('tests:question_create', kwargs={'test_pk': test_pk}), data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful form submission

    def test_question_update_view(self):
        question = Question.objects.create(text='Test Question Text', test=self.test, type=self.question_type)
        response = self.client.get(reverse('tests:question_edit', kwargs={'pk': question.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/question_form.html')

    def test_question_update_post(self):
        question = Question.objects.create(text='Test Question Text', test=self.test, type=self.question_type)
        data = {'text': 'Updated Question Text new', 'test': self.test.pk, 'type': self.question_type.pk}
        response = self.client.post(reverse('tests:question_edit', kwargs={'pk': question.pk}), data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful form submission

    def test_question_detail_view(self):
        question = Question.objects.create(text='Test Question Text', test=self.test, type=self.question_type)
        response = self.client.get(reverse('tests:question_view', kwargs={'pk': question.pk}))
        self.assertEqual(response.status_code, 200)


class AnswersViewTest(TestCase):

    def setUp(self):
        # Create a superuser for testing
        self.user = User.objects.create_superuser(email='admin@example.com', password='adminpass')
        self.client.login(email='admin@example.com', password='adminpass')

        # Create a Chapter for testing
        self.chapter = Chapter.objects.create(title='Test Chapter', description='Test Chapter')

        # Create a Material for testing
        self.material = Material.objects.create(topic='Test Material', text='Test Material', chapter=self.chapter)

        # Create a Test for testing
        self.test = Test.objects.create(
            title='Test Test',
            description='Test Description',
            material=self.material,
            owner=self.user
        )

        # Create a test QuestionType
        self.question_type = QuestionType.objects.create(title='normal')

        # Create a test Question
        self.question = Question.objects.create(text='Test Question Text', test=self.test, type=self.question_type)

    def test_answers_create_view(self):
        response = self.client.get(reverse('tests:answers_create', kwargs={'question_pk': self.question.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tests/answers_form.html')

    def test_answers_create_post(self):
        data = {'text': 'Test Answer Text', 'question': self.question.pk, 'is_correst': True}
        response = self.client.post(reverse('tests:answers_create', kwargs={'question_pk': self.question.pk}), data)
        self.assertEqual(response.status_code, 302)  # Should redirect after successful form submission

    def test_answers_delete_view(self):
        answer = Answers.objects.create(text='Test Answer Text', question=self.question, is_correct=True)
        response = self.client.get(
            reverse('tests:answers_delete', kwargs={'question_pk': self.question.pk, 'pk': answer.pk}))
        self.assertEqual(response.status_code, 200)

    def test_answers_delete_post(self):
        answer = Answers.objects.create(text='Test Answer Text', question=self.question, is_correct=True)
        response = self.client.post(
            reverse('tests:answers_delete', kwargs={'question_pk': self.question.pk, 'pk': answer.pk}))
        self.assertEqual(response.status_code, 302)  # Should redirect after successful deletion
