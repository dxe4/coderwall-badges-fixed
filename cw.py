from selenium import webdriver
from time import sleep
import getpass
from selenium.webdriver.support.wait import WebDriverWait


def run(driver, username, password):
    def find(selector, single=True):
        if single:
            return driver.find_element_by_css_selector(selector)
        else:
            return driver.find_elements_by_css_selector(selector)


    def find_click(selector):
        return driver.find_element_by_css_selector(selector).click()


    def type(selector, _input):
        elm = find(selector)
        elm.click()
        elm.clear()
        elm.send_keys(_input)


    def login_github():
        type("#login_field", username)
        type("#password", password)
        find_click(".auth-form-body .button")


    def save_settings():
        find_click("a[href*=settings]")
        find_click("#user_join_badge_orgs")
        find_click("input[value=Save]")


    def publish(link):
        driver.get(link)
        find_click(".org-module-link[href*=members]")
        type(".auto-search-input", username)
        l = lambda _driver: _driver.find_element_by_css_selector("a[href*=publicize]")
        elm = WebDriverWait(driver, 25).until(l)
        elm.click()

    driver.get("http://www.coderwall.com")
    find_click(".sign-up-panel .github")
    login_github()
    save_settings()
    save_settings()

    driver.get("http://www.github.com/%s" % username)
    sleep(10)
    driver.get("http://www.github.com/%s" % username)

    elms = find(".avatars a[href*=coderwall]", single=False)
    initial = [i.get_attribute("href") for i in elms]

    for href in initial:
        publish(href)

    driver.get("http://www.github.com/%s" % username)
    elms = find(".avatars a[href*=coderwall]", single=False)
    double_check = [i.get_attribute("href") for i in elms]
    new_list = [i for i in double_check if not i in initial]
    if new_list:
        for href in new_list:
            publish(href)


if __name__ == '__main__':
    username = input("github username\n")
    password = getpass.getpass("github password\n")
    driver = webdriver.Firefox()
    try:
        run(driver, username, password)
    except Exception as e:
        print(e)

    driver.close()