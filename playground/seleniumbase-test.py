from seleniumbase import SB

with SB(uc=True, xvfb=True) as sb:
    sb.driver.uc_open_with_reconnect("https://de.indeed.com/?r=us", 20)
    print(sb.driver.title)
    sb.driver.quit()
    sb.xvfb.close()