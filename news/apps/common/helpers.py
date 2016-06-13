import re

from news.utils.str import filename64hex, number64hex


def get_files_upload_path(instance, filename):
    print filename
    extension = re.search(r'\..{3,4}$', filename).group()
    name = filename64hex(filename, 30)
    user = number64hex(instance.author.id, 60)
    return '{0}/{1}{2}'.format(user, name, extension)
