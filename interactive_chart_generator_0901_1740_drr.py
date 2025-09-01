# 代码生成时间: 2025-09-01 17:40:37
# interactive_chart_generator.py

"""
Interactive Chart Generator using Pyramid framework.
This application allows users to generate interactive charts based on provided data.
"""

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
import json

# Import necessary modules for chart generation
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.io import curdoc

# Define the chart generation function
def generate_chart(data):
    """
    Generate an interactive chart based on provided data.
    :param data: A list of dictionaries containing 'x' and 'y' values.
    :return: A tuple containing the chart script and div.
    """
    try:
        # Create a new plot with a title and axis labels
        p = figure(title="Interactive Chart", x_axis_label='x', y_axis_label='y')

        # Add a line renderer with a glyph renderer
        p.line('x', 'y', source=ColumnDataSource(data))

        # Generate the script and div for the chart
        script, div = components(p)
        return script, div
    except Exception as e:
        return "Error generating chart: " + str(e)

# Define the view for the root of the application
@view_config(route_name='home', renderer='templates/home.jinja2')
def home(request):
    """
    The view for the root of the application.
    It renders the home page with a form to submit chart data.
    """
    return {}

# Define the view to handle chart data submission
@view_config(route_name='submit_chart', renderer='json')
def submit_chart(request):
    """
    The view to handle chart data submission.
    It generates an interactive chart based on the submitted data and returns the chart script and div.
    """
    data = request.json_body
    script, div = generate_chart(data)
    return {'chart_script': script, 'chart_div': div}

# Initialize the Pyramid application
def main(global_config, **settings):
    """
    Initialize the Pyramid application.
    """
    with Configurator(settings=settings) as config:
        config.add_route('home', '/')
        config.add_route('submit_chart', '/submit_chart')
        config.scan()

# Run the application if this script is executed directly
if __name__ == '__main__':
    main({"here": here})
