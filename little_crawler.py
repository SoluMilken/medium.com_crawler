import re
from os.path import join

import requests
from bs4 import BeautifulSoup
import validators

from bistiming import IterTimer, SimpleTimer


ROOT_URL = "https://blog.yoctol.com/"
STORY_OUTPUT_DIR = "/home/en/nlp_share/corpus/yoctol/"


def get_stories_urls():
    result = requests.get(ROOT_URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    for class_a_content in soup.find_all('a'):
        url_split_lst = re.split("https://blog.yoctol.com/", class_a_content['href'])
        if len(url_split_lst) == 2:
            if len(url_split_lst[1]) > 10:
                yield class_a_content['href']


def save_story(datetime_str, title_str, document_str):
    output_filename = datetime_str + "_" + title_str + ".txt"
    with SimpleTimer("Saving stories to {}".format(output_filename)):
        with open(join(STORY_OUTPUT_DIR, output_filename), "w") as writer:
            writer.write(document_str)


def get_stories_text():
    for story_url in get_stories_urls():
        if validators.url(story_url):
            result = requests.get(story_url)
            if result.status_code == requests.codes.ok:
                soup = BeautifulSoup(result.text, 'html.parser')
                if len(soup.find_all('p')) > 0:
                    document = ''
                    for class_p_content in soup.find_all('p'):
                        document += class_p_content.get_text()
                    save_story(
                        datetime_str=str(soup.time).split("\"")[1],
                        title_str=soup.title.get_text(),
                        document_str=document)



if __name__ == '__main__':
    get_stories_text()
