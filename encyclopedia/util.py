import re
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import markdown2

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    try:
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            return False
        #     default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))
        return True
    except(err):
        print(err)
        return False


def change_entry(title, content):
    try:
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))
        return True
    except(err):
        print(err)
        return False


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def markdown_to_html(title):
    try:
        entry = get_entry(title)
        return markdown2.markdown(entry)
    except:
        return None

def get_random_page():
    file_names = list_entries()
    random_element = random.choice(file_names)
    return random_element
