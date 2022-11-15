import requests


def download_file(url, filepath):
    response = requests.get(url)

    with open(filepath, "wb") as file:
        file.write(response.content)

    print("Saved {} as {}".format(url, filepath))
