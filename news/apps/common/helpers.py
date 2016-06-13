

def get_files_upload_path(instance, filename):
    return '{0}/{1}'.format(instance.author.id, filename)
