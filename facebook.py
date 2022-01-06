from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import numeric_times
import selenium_objects
from state import State
import datetime
import time
import random
import notifier
import traceback


def init():
    notifier.notify("Loading...", "   ")
    State.load()
    if State.last_checked_date == str(datetime.date.today()):
        notifier.notify('Notifications', 'Already updated today!')
        selenium_objects.client.quit()
        exit()
    Account.login()


def get_latest_posts():
    latest_posts = []
    base_url = "https://mbasic.facebook.com"
    for profile_path in State.profiles_paths:
        try:
            print('Processing profile: ' + profile_path)
            profile_latest_posts = profile.get_latest_posts(
                base_url+profile_path)
            print(profile_latest_posts)
            latest_posts.extend(profile_latest_posts)
        except:
            notifier.notify(
                'An Error Occured', traceback.format_exc() + f"\nProfile: {profile_path}")
            pass
    print('Quitting Client...')
    selenium_objects.client.quit()
    print('Updating State...')
    State.update()
    return latest_posts


class Account:

    def login():
        selenium_objects.client.get("https://www.facebook.com/me/")

        # get the logged_in cookie
        logged_in_cookie = selenium_objects.client.get_cookie('c_user')
        # check if already logged in
        if logged_in_cookie != None:
            # print(logged_in_cookie)
            print('Already logged in!')
            return True
        # login
        print("Logging in....")
        selenium_objects.client.find_element(By.ID, 'email').send_keys(
            State.email)
        selenium_objects.client.find_element(By.ID, 'pass').send_keys(
            State.password + Keys.ENTER)
        selenium_objects.wait.until(lambda client: client.get_cookie('c_user')
                                    if client.get_cookie('c_user') != None else False)
        # print(selenium_objects.client.get_cookie('c_user'))
        return True


class profile:

    def get_latest_posts(profile_link, profile_name=None):
        # sleep for a few seconds,
        # so that Facebook doesn't block you for spamming!!
        time.sleep(random.randint(3, 6))
        # go to the profile page
        selenium_objects.client.get(profile_link)
        # get the profile name
        if profile_name == None:
            profile_name = selenium_objects.client.title
            # print(profile_name)
        # get the post list
        posts_elements = selenium_objects.client.find_elements_by_tag_name(
            'article')

        latest_posts = []
        loop_is_broken = False

        for post_element in posts_elements:
            try:
                post_title = post_element.find_element_by_tag_name(
                    'p').get_attribute('textContent')
                # print(post_title)
                post_time = post_element.find_element_by_tag_name(
                    'abbr').get_attribute('textContent')
                # print(post_time)
                # check if time is later
                # if later, add it to the new posts list
                try:
                    post_numeric_time = numeric_times.get_numeric_time(
                        post_time)
                    if post_numeric_time > State.last_checked_time:
                        # print('post should exist')
                        latest_posts.append({
                            "profile_name": profile_name,
                            "post_title": post_title,
                            "post_time": post_time
                        })
                    else:
                        loop_is_broken = True
                        break
                        # if not, set loop_broken to True and break the loop
                except:
                    pass
            except NoSuchElementException:
                pass

        # print(latest_posts)
        try:
            if not loop_is_broken:
                # go to next page and repeat
                next_page_link_element = selenium_objects.client.find_element_by_partial_link_text(
                    'See More Stories')
                next_page_link = next_page_link_element.get_attribute('href')
                latest_posts.extend(profile.get_latest_posts(
                    next_page_link, profile_name))

            return latest_posts
        except NoSuchElementException:
            pass
        except:
            notifier.notify('An Error Occured', traceback.format_exc())
            pass
