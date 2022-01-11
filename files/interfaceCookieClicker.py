import time
import threading
from Bot import Bot


class InterfaceCookieClicker(Bot):
    def __init__(self, fullscreen):
        self.at_main_game = True
        self.clicking = False
        self.last_save = time.time()
        self.minutes_to_save = 2
        self.lock = threading.Lock()
        super().__init__(fullscreen=fullscreen)

    def mission(self):
        self.get('https://orteil.dashnet.org/cookieclicker/')
        # self.driver.fullscreen_window()
        self.load_game()
        threading.Thread(target=self.click_on_cookie).start()
        threading.Thread(target=self.make_upgrades).start()
        threading.Thread(target=self.buy_helpers).start()
        threading.Thread(target=self.save_game).start()

    def click_on_cookie(self, seconds=30, sleep_time=5):
        while True:
            try:
                cookie = self.find_element_by_xpath('//*[@id="bigCookie"]')
                start_click = time.time()
                while (time.time() - start_click) < seconds:
                    with self.lock:
                        cookie.click()
            except Exception as e:
                print(f'erro {e} no click on cookie')

    def make_upgrades(self):
        while True:
            enabled_update = self.find_element_by_xpath('//div[@class="crate upgrade enabled"]', false_on_not_found=True, timeout=1)
            if enabled_update:
                with self.lock:
                    try:
                        enabled_update.click()
                    except Exception as e:
                        print(f'erro {e} no make upgrades')

    def buy_helpers(self):
        while True:
            enabled_helper = self.find_element_by_xpath('//div[@class="product unlocked enabled"]', false_on_not_found=True, timeout=1)
            if enabled_helper:
                with self.lock:
                    try:
                        enabled_helper.click()
                    except Exception as e:
                        print(f'erro {e} no buy helpers')

    def load_game(self):
        time.sleep(1)
        self.click_on_element('//*[@id="prefsButton"]')
        self.click_on_element('//*[@id="menu"]/div[3]/div[3]/a[2]')
        time.sleep(1) # TODO: Discover why is needed
        save_code = open('save', 'r').read()
        self.send_keys('//*[@id="textareaPrompt"]', save_code)
        self.click_on_element('//*[@id="promptOption0"]')
        time.sleep(1)
        self.click_on_element('//*[@id="menu"]/div[1]')
        time.sleep(1)

    def save_game(self):
        while True:
            try:
                if (time.time() - self.last_save) / 60 > self.minutes_to_save:
                    with self.lock:
                        time.sleep(1)
                        self.click_on_element('//*[@id="prefsButton"]')
                        self.click_on_element('//*[@id="menu"]/div[3]/div[3]/a[1]')
                        new_save_code = self.get_text_from_element('//*[@id="textareaPrompt"]')
                        open('save', 'w').write(new_save_code)
                        self.click_on_element('//*[@id="promptOption0"]')
                        self.click_on_element('//*[@id="menu"]/div[1]')
                        self.last_save = time.time()
            except Exception as e:
                print(f'erro {e} no save game')



