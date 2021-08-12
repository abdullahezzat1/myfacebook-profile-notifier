import selenium_objects
import traceback
import notifier
import facebook

try:
    facebook.init()

    latest_posts = facebook.get_latest_posts()

    if len(latest_posts) == 0:
        notifier.notify("No new notifications today!", "Facebook Notifier")
        exit()

    # print(latest_posts)

    notifier.notify_list(latest_posts)

except SystemExit as e:
    selenium_objects.client.quit()
    exit(e)

except:
    notifier.notify('An Error Occured', traceback.format_exc())
    selenium_objects.client.quit()
