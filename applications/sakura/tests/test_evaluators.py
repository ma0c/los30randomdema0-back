from django.test import TestCase
from applications.sakura.models import Question, EXACT, TERMS, tokenize


class TestEvaluators(TestCase):
    def setUp(self):
        self.exact_question = Question(
            serial_number=1,
            question="What is the capital of France?",
            answer="Paris",
            theme="Geography",
            responsible="ma0",
            evaluation_type=f"{EXACT}",
            slug="what-is-the-capital-of-france"
        )

        self.terms_question = Question(
            serial_number=2,
            question="What are the colors of the French flag?",
            answer="blue white red",
            theme="Geography",
            responsible="ma0",
            evaluation_type=f"{TERMS} 3/3",
            slug="what-are-the-colors-of-the-french-flag"
        )

        self.last_name_question = Question(
            serial_number=3,
            question="What is the name of the current president of the United States?",
            answer="Biden",
            theme="Geography",
            responsible="ma0",
            evaluation_type=f"{TERMS} 1/1",
            slug="what-is-the-last-name-of-the-current-president-of-the-united-states"
        )

        self.accent_question = Question(
            serial_number=4,
            question="Revolution in spanish",
            answer="Revolución",
            theme="Geography",
            responsible="ma0",
            evaluation_type=f"{EXACT}",
            slug="what-is-the-capital-of-france"
        )
        self.accent_terms_question = Question(
            serial_number=4,
            question="Poetic Improvisation in spanish",
            answer="Improvisación Poética",
            theme="Geography",
            responsible="ma0",
            evaluation_type=f"{TERMS} 2/2",
            slug="what-is-the-capital-of-france"
        )

    def test_exact(self):
        assert self.exact_question.evaluate_question("Paris")

    def test_exact_lower(self):
        assert self.exact_question.evaluate_question("paris")

    def test_exact_fail(self):
        assert not self.exact_question.evaluate_question("London")

    def test_terms(self):
        self.terms_question.evaluation_type = f"{TERMS} 2/3"
        assert self.terms_question.evaluate_question("blue white")

    def test_extra_terms(self):
        assert self.terms_question.evaluate_question("blue white and red")

    def test_terms_comma(self):
        assert self.terms_question.evaluate_question("blue, white and red")


    def test_terms_dash(self):
        assert self.terms_question.evaluate_question("blue-white-red")

    def test_last_name(self):
        assert self.last_name_question.evaluate_question("Joe Biden")

    def test_accent(self):
        assert self.accent_question.evaluate_question("revolucion")

    def test_terms_accent(self):
        assert self.accent_terms_question.evaluate_question("improvisacion poetica")