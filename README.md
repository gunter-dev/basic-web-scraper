# Basic web scraper in Python

This is the implementation of a basic web scraper, that takes multiple links as an input
and searches for all the URLs on that specific website.

## Usage

Make a txt file of links separated by new line characters and name it whatever you want to.
Then start the Python script like this:

```bash
$ python3 main.py <input_file> <output_file>
```

Where `input_file` is the name of the file you created with all your desired URLs and
`output_file` is the name of the file you want to save all the links to. For testing
purposes you can use `sample_links.txt` as the input file to see how it behaves,
but you can certainly create your own file.

Both arguments are required and the application will terminate if you don't provide them.

## Prerequisisties

Developed with Python version 3.10.11. The packages needed can be installed using 
the `requirements.txt` file like this:

```bash
$ pip install -r requirements.txt
```

## Unit tests

You can also launch unit tests (no arguments needed):

```bash
$ python3 unit_tests.py
```
