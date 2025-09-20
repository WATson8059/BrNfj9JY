# 代码生成时间: 2025-09-20 17:26:50
from pyramid.config import Configurator
from pyramid.response import Response
import os
import re
from collections import Counter

"""
Text File Analyzer

This program analyzes the content of a text file, providing word frequency and other insights.
"""


class SimpleFileAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.word_freq = Counter()
    
    def read_file(self):
        """Reads the file and updates the word frequency counter."""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    words = re.findall(r'\w+', line.lower())
                    self.word_freq.update(words)
        except FileNotFoundError:
            print(f"Error: The file at {self.filepath} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    def get_word_frequency(self):
        """Returns the word frequency count."""
        return dict(self.word_freq)


def main(global_config, **settings):
    """
    This function sets up the Pyramid application.
    """
    config = Configurator(settings=settings)
    config.add_route('analyze', '/analyze')
    config.add_view(analyze_text_file, route_name='analyze', renderer='json')
    return config.make_wsgi_app()


def analyze_text_file(request):
    """
    An endpoint to analyze a text file and return word frequencies.
    """
    file_path = request.params.get('filepath')
    if not file_path or not os.path.isfile(file_path):
        return Response(
           {"error": "Please provide a valid file path."},
           content_type='application/json',
           status=400)
    analyzer = SimpleFileAnalyzer(file_path)
    analyzer.read_file()
    word_freq = analyzer.get_word_frequency()
    return {'word_count': word_freq}
