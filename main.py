from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from prometheus_client import Gauge, start_http_server
import time

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
var FPS = prometheus.NewGauge(
   prometheus.GaugeOpts{
       Name: "average FPS",
       Help: "amount of rendering frames per second",
   },
)

try:
    duration_seconds = 10   
    driver.get('https://google.com')
    textarea = driver.find_element(By.CSS_SELECTOR, 'textarea')
    textarea.send_keys('Example search')
    textarea.send_keys(Keys.RETURN) 

    start_time = time.time()
    fps_values = []

    while time.time() - start_time < duration_seconds:
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.ARROW_DOWN)
        fps = driver.execute_script(js_script)
        print(fps)
        fps_values.append(fps)
        time.sleep(1)

    average_fps = sum(fps_values) / len(fps_values)
    g.set(average_fps)
    print(f'Средний ФПС за {duration_seconds} секунд: {average_fps:.2f}')
except Exception as e:
    print(f"Ошибка: {str(e)}")
finally:
    driver.quit()
