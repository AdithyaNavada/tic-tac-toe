import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

BASE_URL = "http://localhost:5000"
PAUSE = 1.5 

@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=414,896")  
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    service = Service(ChromeDriverManager().install())

    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(2)
    yield drv
    drv.quit()


def by_testid(driver_or_wait, testid):
    return (By.CSS_SELECTOR, f'[data-testid="{testid}"]')


def click_testid(driver, testid, timeout=5):
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-testid="{testid}"]'))
    )
    el.click()
    return el


def wait_visible(driver, testid, timeout=5):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-testid="{testid}"]'))
    )


def test_welcome_screen_loads(driver):
    driver.get(BASE_URL)
    heading = wait_visible(driver, "screen-welcome")
    assert heading.is_displayed()
    assert "Tic Tac Toe" in driver.title or "Tic" in driver.page_source


def test_full_friend_vs_friend_game_to_a_win(driver):
    driver.get(BASE_URL)
    click_testid(driver, "btn-enter")
    wait_visible(driver, "screen-mode")
    click_testid(driver, "btn-vs-friend")

    wait_visible(driver, "screen-game")

    move_sequence = [0, 3, 1, 4, 2]
    for idx in move_sequence:
        click_testid(driver, f"cell-{idx}")
        time.sleep(0.15)  

    status = wait_visible(driver, "status-line")
    assert "wins" in status.text.lower()

    winning_cells = [driver.find_element(*by_testid(driver, f"cell-{i}")) for i in (0, 1, 2)]
    assert all("win" in c.get_attribute("class") for c in winning_cells)

    play_again = wait_visible(driver, "btn-play-again")
    assert play_again.is_displayed()


def test_vs_computer_easy_game_completes(driver):
    driver.get(BASE_URL)
    click_testid(driver, "btn-enter")
    wait_visible(driver, "screen-mode")
    click_testid(driver, "btn-vs-computer")
    wait_visible(driver, "difficulty-picker")
    click_testid(driver, "difficulty-easy")

    wait_visible(driver, "screen-game")

    for _ in range(9):
        status = driver.find_element(*by_testid(driver, "status-line")).text.lower()
        if "win" in status or "draw" in status:
            break
        cells = driver.find_elements(By.CSS_SELECTOR, ".cell:not(.filled)")
        if not cells:
            break
        cells[0].click()
        time.sleep(0.4)  

    final_status = driver.find_element(*by_testid(driver, "status-line")).text.lower()
    assert "win" in final_status or "draw" in final_status


def test_reset_clears_board(driver):
    driver.get(BASE_URL)
    click_testid(driver, "btn-enter")
    click_testid(driver, "btn-vs-friend")
    wait_visible(driver, "screen-game")

    click_testid(driver, "cell-0")
    time.sleep(0.2)
    filled_before = driver.find_elements(By.CSS_SELECTOR, ".cell.filled")
    assert len(filled_before) == 1

    click_testid(driver, "game-reset")
    time.sleep(0.2)
    filled_after = driver.find_elements(By.CSS_SELECTOR, ".cell.filled")
    assert len(filled_after) == 0



def play_full_game_vs_computer(driver):
    for _ in range(9):
        status_text = driver.find_element(
            By.CSS_SELECTOR, '[data-testid="status-line"]'
        ).text.lower()
        if "win" in status_text or "draw" in status_text:
            break
        cells = driver.find_elements(By.CSS_SELECTOR, ".cell:not(.filled)")
        if not cells:
            break
        time.sleep(PAUSE)
        cells[0].click()
        time.sleep(PAUSE)

def test_full_slow_walkthrough_all_modes(driver):
    driver.get(BASE_URL)
    wait_visible(driver, "screen-welcome")
    click_testid(driver, "btn-enter")
    wait_visible(driver, "screen-mode")
    click_testid(driver, "btn-vs-friend")
    wait_visible(driver, "screen-game")
    for idx in [0, 3, 1, 4, 2]:
        click_testid(driver, f"cell-{idx}")
        time.sleep(PAUSE)
    status = wait_visible(driver, "status-line")
    assert "wins" in status.text.lower()
    print(f"\n[Friend mode] Result: {status.text}")
    click_testid(driver, "game-back")
    wait_visible(driver, "screen-mode")
    click_testid(driver, "btn-vs-computer")
    wait_visible(driver, "difficulty-picker")
    click_testid(driver, "difficulty-easy")
    wait_visible(driver, "screen-game")
    play_full_game_vs_computer(driver)
    result_easy = driver.find_element(By.CSS_SELECTOR, '[data-testid="status-line"]').text
    print(f"[Easy] Result: {result_easy}")
    assert "win" in result_easy.lower() or "draw" in result_easy.lower()
    click_testid(driver, "game-back")
    wait_visible(driver, "screen-mode")
    click_testid(driver, "btn-vs-computer")
    wait_visible(driver, "difficulty-picker")
    click_testid(driver, "difficulty-medium")
    wait_visible(driver, "screen-game")
    play_full_game_vs_computer(driver)
    result_medium = driver.find_element(By.CSS_SELECTOR, '[data-testid="status-line"]').text
    print(f"[Medium] Result: {result_medium}")
    assert "win" in result_medium.lower() or "draw" in result_medium.lower()
    click_testid(driver, "game-back")
    wait_visible(driver, "screen-mode")
    click_testid(driver, "btn-vs-computer")
    wait_visible(driver, "difficulty-picker")
    click_testid(driver, "difficulty-hard")
    wait_visible(driver, "screen-game")
    play_full_game_vs_computer(driver)
    result_hard = driver.find_element(By.CSS_SELECTOR, '[data-testid="status-line"]').text
    print(f"[Hard] Result: {result_hard}")
    assert "win" in result_hard.lower() or "draw" in result_hard.lower()
    time.sleep(PAUSE * 2)