import plugintypes
import tgl
from telegrambot.utils.decorators import group_only
import requests
from bs4 import BeautifulSoup


class FSMKPlugin(plugintypes.TelegramPlugin):
    """
    FSMK tasks
    """

    patterns = {
        "^/feed$":"get_planet",
        "^/updates$":"get_updates",
        "^/task$":"get_tasks",
        ".*\b(f|F)ree\b(?!beer|drinks?).*":"free_freedom",
    }

    usage = [
        "/feed: pull content from planet",
        "/updates: pull updates from fsmk.org",
        "/task: get task list",
    ]

    def __init__(self):
        super().__init__()


    @group_only
    def get_planet(self, msg, matches):
        soup = BeautifulSoup(requests.get("http://fsmk.org/planet/").text)
        posts = soup.findAll('li', {"class":"odd"})
        text = "Last 5 posts in planet:\n"
        for post in posts[:5]:
            text+="* %s by %s %s\n" % (post.div.a.text, post.find('div', {"class":"name"}).a.text, post.div.a['href'])
        return text

    @group_only
    def get_updates(self, msg, matches):
        soup = BeautifulSoup(requests.get("http://fsmk.org/").text)
        posts = soup.findAll('a')
        text = "Last 3 updates on fsmk.org:\n"
        updcount = 0
        for post in posts:
            if updcount == 3:
                break
            if post['href'].startswith("/updates/"):
                text+="* %s %s\n" % (post.text, "http://beta.fsmk.org"+post['href'])
                updcount += 1
        return text

    @group_only
    def get_tasks(self, msg, matches):
        return "Tasks pad not defined yet"

    @group_only
    def free_freedom(self, msg, matches):
        return "(as in freedom)"
