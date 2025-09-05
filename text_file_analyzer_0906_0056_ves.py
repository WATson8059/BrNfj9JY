# 代码生成时间: 2025-09-06 00:56:34
import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.request import Request
from pyramid.session import check_csrf_token
from pyramid.exceptions import HTTPBadRequest
import nltk
import string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re


def get_stop_words():
    # Get the list of stop words from NLTK
    return set(stopwords.words('english'))


def clean_text(text):
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    return text


def tokenize(text):
    # Tokenize the text into words
    return word_tokenize(text)


def remove_stop_words(words, stop_words):
    # Remove stop words from the tokenized words
    return [word for word in words if word not in stop_words]


def analyze_text(file_path, output_format='text'):
    """
    Analyze the text file and return the analysis in the specified format.
    :param file_path: Path to the text file to analyze.
    :param output_format: Format of the output. Can be 'text' or 'json'.
    :return: Analysis of the text file in the specified format.
    """
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        stop_words = get_stop_words()
        text = clean_text(text)
        tokens = tokenize(text)
        filtered_tokens = remove_stop_words(tokens, stop_words)
        token_counts = Counter(filtered_tokens)

        if output_format == 'text':
            return '
'.join(f'{word}: {count}' for word, count in token_counts.most_common(10))
        elif output_format == 'json':
            return json.dumps({word: count for word, count in token_counts.most_common(10)})
        else:
            raise ValueError('Invalid output format')
    except FileNotFoundError:
        return 'File not found', 404
    except Exception as e:
        return f'An error occurred: {e}', 500

# Pyramid app setup
def main(global_config, **settings):
    """
    Pyramid WSGI application entry point.
    :param global_config: Pyramid global configuration.
    :param settings: Application settings.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_renderer('html', render_to_response)
    config.add_route('analyze', '/analyze')
    config.scan()
    return config.make_wsgi_app()

# Pyramid views
@view_config(route_name='analyze', renderer='json')
def analyze_view(request: Request):
    """
    View to handle text analysis requests.
    :param request: Pyramid request object.
    """
    if 'file' not in request.POST:
        raise HTTPBadRequest('No file provided')
    file = request.POST['file'].file
    file_path = '/tmp/uploaded_file.txt'
    with open(file_path, 'wb') as f:
        f.write(file.read())
    analysis = analyze_text(file_path, output_format='json')
    return {'analysis': analysis}
