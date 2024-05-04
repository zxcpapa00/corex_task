from tasks.models import Question


class TestAnalytics:
    @staticmethod
    def get_pass_count(test_id):
        pass_count = Question.objects.filter(test_id=test_id).count()
        return pass_count

    @staticmethod
    def get_success_rate(test_id):
        total_questions = Question.objects.filter(test_id=test_id).count()
        correct_answers = Question.objects.filter(test_id=test_id, correct_answer=True).count()
        success_rate = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        return success_rate

    @staticmethod
    def get_hardest_question(test_id):
        hardest_question = Question.objects.filter(test_id=test_id).order_by('id').first()
        return hardest_question.text if hardest_question else None
