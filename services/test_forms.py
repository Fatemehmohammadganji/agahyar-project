import pytest
from services.forms import CITY_CHOICES, RegisterForm


class TestCityChoices:

    def test_city_choices_has_placeholder_first(self):
        assert CITY_CHOICES[0] == ('', 'شهر خود را انتخاب کنید')

    def test_city_choices_contains_tehran(self):
        assert ('تهران', 'تهران') in CITY_CHOICES

    def test_city_choices_count(self):
        assert len(CITY_CHOICES) == 13

    def test_register_form_uses_city_choices(self):
        form = RegisterForm()
        city_field = form.fields['city']
        widget = city_field.widget
        assert widget.choices == CITY_CHOICES


@pytest.mark.django_db
class TestRegisterForm:

    def test_form_renders_city_field(self):
        form = RegisterForm()
        html = str(form.as_p())
        assert 'تهران' in html
        assert 'مشهد' in html
