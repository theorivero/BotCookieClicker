import time
import threading
from Bot import Bot


class InterfaceCookieClicker(Bot):
    def __init__(self, fullscreen):
        self.at_main_game = True
        self.clicking = False
        self.last_save = time.time()
        self.minutes_to_save = 2
        super().__init__(fullscreen=fullscreen)

    def mission(self):
        self.get('https://orteil.dashnet.org/cookieclicker/')
        # self.driver.fullscreen_window()
        self.load_game()
        while True:
            try:
                self.click_on_cookie()
                self.make_upgrades()
                self.buy_helpers()
                self.save_game()
            except Exception as e:
                pass


    def click_on_cookie(self, seconds=10, sleep_time=5):
        if self.at_main_game:
            self.clicking = True
            cookie = self.find_element_by_xpath('//*[@id="bigCookie"]')
            start_click = time.time()
            while (time.time() - start_click) < seconds:
                cookie.click()
            self.clicking = False
            # time.sleep(sleep_time)
        else:
            print('Não foi possivel clicar agora, tentando mais tarde')
            # time.sleep(sleep_time)

    def make_upgrades(self):
        enabled_update = self.find_element_by_xpath('//div[@class="crate upgrade enabled"]', false_on_not_found=True, timeout=1)
        while enabled_update:
            enabled_update.click()
            enabled_update = self.find_element_by_xpath('//div[@class="crate upgrade enabled"]', false_on_not_found=True, timeout=1)

    def buy_helpers(self):
        enabled_helper = self.find_element_by_xpath('//div[@class="product unlocked enabled"]', false_on_not_found=True, timeout=1)
        while enabled_helper:
            enabled_helper.click()
            enabled_helper = self.find_element_by_xpath('//div[@class="product unlocked enabled"]', false_on_not_found=True, timeout=1)

    def load_game(self):
        self.at_main_game = False
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
        self.at_main_game = True

    def save_game(self):
        while self.clicking:
            time.sleep(0.3)
        if (time.time() - self.last_save) / 60 > self.minutes_to_save:
            self.at_main_game = False
            time.sleep(1)
            self.click_on_element('//*[@id="prefsButton"]')
            self.click_on_element('//*[@id="menu"]/div[3]/div[3]/a[1]')
            new_save_code = self.get_text_from_element('//*[@id="textareaPrompt"]')
            open('save', 'w').write(new_save_code)
            self.click_on_element('//*[@id="promptOption0"]')
            self.click_on_element('//*[@id="menu"]/div[1]')
            self.last_save = time.time()
            time.sleep(1)
            self.at_main_game = True



