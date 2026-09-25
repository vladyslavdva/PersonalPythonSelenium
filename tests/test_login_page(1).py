import pytest

from page_objects.login_page import LoginPage


class TestLogin:
    @pytest.mark.positive_login
    @pytest.mark.parametrize(
        ("username", "password"),
        [("student", "Password123")],
    )
    def test_positive_login(self, driver, base_url, username, password):
        login_page = LoginPage(driver, base_url)
        login_page.open()
        login_page.login(username, password)

        assert login_page.success_message == LoginPage.SUCCESS_MESSAGE
        assert login_page.current_url == login_page.success_url
        assert login_page.logout_link_is_visible
