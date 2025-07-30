from yf_driver import start_driver, open_yf_and_accept_cookies, close_driver

def main():
    driver = start_driver(headless=True)
    open_yf_and_accept_cookies(driver)
    close_driver(driver)

if __name__ == "__main__":
    main()
