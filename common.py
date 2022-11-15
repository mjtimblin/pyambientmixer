import requests


def download_file(url, filepath):
    response = requests.get(url)

    with open(filepath, "wb") as file:
        file.write(response.content)

    print("Saved {} as {}".format(url, filepath))


def make_filesafe(s: str):
    return ''.join([c for c in s.replace(' ', '_') if
                    c.isalpha() or c.isdigit() or c == '_' or c == '-']).rstrip()
