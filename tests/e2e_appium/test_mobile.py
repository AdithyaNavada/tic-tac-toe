import time
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

APPIUM_SERVER = "http://127.0.0.1:4723"
BASE_URL = "http://10.140.152.230:5000"


@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.browser_name = "Chrome"
    options.new_command_timeout = 120
    options.set_capability("appium:ignoreHiddenApiPolicyError", True)
    options.set_capability("appium:noReset", True)
    options.set_capability("appium:chromeOptions", {"androidUseRunningApp": True})

    drv = webdriver.Remote(APPIUM_SERVER, options=options)
    drv.implicitly_wait(3)
    yield drv
    drv.quit()


def click_testid(driver, testid, timeout=8):
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="{testid}"]'))
    )
    el.click()
    return el


def wait_visible(driver, testid, timeout=8):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{testid}"]'))
    )


def test_app_loads_on_mobile_browser(driver):
    driver.get(BASE_URL)
    welcome = wait_visible(driver, "screen-welcome")
    assert welcome.is_displayed()


def test_full_friend_vs_friend_game_on_mobile(driver):
    driver.get(BASE_URL)
    click_testid(driver, "btn-enter")
    wait_visible(driver, "screen-mode")
    click_testid(driver, "btn-vs-friend")
    wait_visible(driver, "screen-game")

    for idx in [0, 3, 1, 4, 2]:
        click_testid(driver, f"cell-{idx}")
        time.sleep(0.2)

    status = wait_visible(driver, "status-line")
    assert "wins" in status.text.lower()


def test_vs_computer_on_mobile_completes(driver):
    driver.get(BASE_URL)
    click_testid(driver, "btn-enter")
    wait_visible(driver, "screen-mode")
    click_testid(driver, "btn-vs-computer")
    wait_visible(driver, "difficulty-picker")
    click_testid(driver, "difficulty-medium")
    wait_visible(driver, "screen-game")

    for _ in range(9):
        status_text = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="status-line"]'
        ).text.lower()
        if "win" in status_text or "draw" in status_text:
            break
        cells = driver.find_elements(By.CSS_SELECTOR, ".cell:not(.filled)")
        if not cells:
            break
        cells[0].click()
        time.sleep(0.5)

    final_status = driver.find_element(
        By.CSS_SELECTOR, '[data-testid="status-line"]'
    ).text.lower()
    assert "win" in final_status or "draw" in final_status


def test_pwa_install_prompt_manifest_present(driver):
    driver.get(BASE_URL)
    manifest_link = driver.find_element(By.CSS_SELECTOR, 'link[rel="manifest"]')
    assert manifest_link.get_attribute("href").endswith("manifest.json")
