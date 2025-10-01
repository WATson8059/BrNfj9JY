# 代码生成时间: 2025-10-01 18:26:00
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from pyramid.view import view_config
from pyramid.response import Response
from pyramid例外 import ExceptionResponseFactory
from pyramid.renderers import JSON


# Define a custom Pyramid exception response factory for error handling
exception_response_factory = ExceptionResponseFactory(
    'json',
    dumps=lambda obj, **kw: JSON()({'errors': str(obj)}).serialize(obj, **kw)
)


# Base feature engineering class
class FeatureEngineering:
    """
    A class for feature engineering tasks.
    It includes methods for data scaling, encoding and pipelining.
    """
    def __init__(self, column_names, categorical_columns):
        self.column_names = column_names
        self.categorical_columns = categorical_columns
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder()
        self.transformer = self._create_transformer()
        self.pipeline = self._create_pipeline()

    def _create_transformer(self):
        """
        Create a ColumnTransformer to apply different transformations to different columns.
        """
        return ColumnTransformer(
            transformers=[
                ('num', self.scaler, [col for col in self.column_names if col not in self.categorical_columns]),
                ('cat', self.encoder, self.categorical_columns)
            ]
        )

    def _create_pipeline(self):
        """
        Create a pipeline that includes both transformer and a final estimator.
        Currently, it only includes the transformer.
        """
        return Pipeline(steps=[('transformer', self.transformer)])

    def fit_transform(self, data):
        """
        Fit and transform the data using the pipeline.
        """
        try:
            transformed_data = self.pipeline.fit_transform(data)
            return transformed_data
        except Exception as e:
            raise Exception(f'Error during feature engineering: {str(e)}')


# Pyramid view to handle feature engineering requests
@view_config(route_name='feature_engineering', renderer='json')
def feature_engineering_view(request):
    """
    A Pyramid view to handle feature engineering requests.
    It expects a JSON payload with a pandas DataFrame and column names.
    """
    try:
        # Parse the request payload
        data = request.json_body
        df = pd.DataFrame(data['data'])
        column_names = data.get('column_names')
        categorical_columns = data.get('categorical_columns')

        # Validate input
        if not column_names or not categorical_columns:
            return exception_response_factory(
                ValueError('Column names and categorical columns must be provided.'), request
            )

        # Create and use the feature engineering tool
        feature_engineering_tool = FeatureEngineering(column_names, categorical_columns)
        transformed_data = feature_engineering_tool.fit_transform(df)
        return {'transformed_data': transformed_data.tolist()}
    except Exception as e:
        return exception_response_factory(e, request)
