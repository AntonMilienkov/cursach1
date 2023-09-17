from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Задаем параметры через экземпляр Options, который передадим веб-драйверу
chrome_options = Options()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

# Execute JavaScript to measure FPS
js_script = """
const times = [];
let fps = 0;

function refreshLoop() {
  window.requestAnimationFrame(() => {
    const now = performance.now();
    while (times.length > 0 && times[0] <= now - 1000) {
      times.shift();
    }
    times.push(now);
    fps = times.length;
    refreshLoop();
  });
}

refreshLoop();
return fps;
"""

try:
    duration_seconds = 10   # время в секундах, в течении которого будет работать скрипт

    # переходим на страничку гугл.ком, пишем в поисковую строку Example search и нажимаем ентер
    driver.get('https://google.com')
    textarea = driver.find_element(By.CSS_SELECTOR, 'textarea')
    textarea.send_keys('Example search')
    textarea.send_keys(Keys.RETURN)  # Press Enter

    start_time = time.time()
    fps_values = []

    while time.time() - start_time < duration_seconds:
        # Симулируем скролл страницы результатов поиска и запускаем скрипт из переменной js_script
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.ARROW_DOWN)
        fps = driver.execute_script(js_script)
        print(fps)
        fps_values.append(fps)
        time.sleep(1)

    average_fps = sum(fps_values) / len(fps_values)
    print(f'Средний ФПС за {duration_seconds} секунд: {average_fps:.2f}')
except Exception as e:
    print(f"Ошибка: {str(e)}")
finally:
    driver.quit()
