
def camel_case(text):
    if hasattr(text, 'split'):
        splitted = text.split('_')
        splitted_first = splitted[:1]
        splitted_rest = splitted[1:]
        splitted_rest_title = [x.title() for x in splitted_rest]
        all_together = splitted_first + splitted_rest_title
        return ''.join(all_together)
    return text
