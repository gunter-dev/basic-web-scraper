import sys
import requests

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing import Process, Queue


def is_url_valid(url):
    try:
        response = requests.head(url, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return False

    return True


def producer(queue, input_file_name):
    with open(input_file_name, 'r') as input_file:
        urls = input_file.read().splitlines()

    for url in urls:
        if not is_url_valid(url):
            continue

        response = requests.get(url)

        if response.status_code != 200:
            print("Site at ", url, " is not responding correctly")
            continue

        parsed_markup = BeautifulSoup(response.content, 'html.parser')

        if queue.full():
            queue.get()

        queue.put({"markup": parsed_markup, "url": url})

    queue.put(None)


def consumer(queue, output_file_name):
    with open(output_file_name, 'w') as output_file:
        while True:
            item = queue.get()
            if item is None:
                break

            links = item['markup'].find_all('a')

            output_file.write("Links at " + item['url'] + '\n')

            for link in links:
                href = link.get('href')

                if href and href != 'javascript:void(0)':
                    absolute_url = urljoin(item['url'], href)
                    output_file.write('- ' + absolute_url + '\n')

            output_file.write("=================================================================================\n")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Missing argument! Add the name of the input file and the output file.")
        sys.exit(1)

    q = Queue(maxsize=10)
    p = Process(target=producer, args=[q, sys.argv[1]])
    c = Process(target=consumer, args=[q, sys.argv[2]])

    p.start()
    c.start()

    p.join()
    c.join()
