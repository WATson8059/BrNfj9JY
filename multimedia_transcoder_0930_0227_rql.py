# 代码生成时间: 2025-09-30 02:27:28
# multimedia_transcoder.py
"""
A Pyramid application that acts as a multimedia transcoder.
It demonstrates the usage of Pyramid framework to build a web service.
"""
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import subprocess
import mimetypes
import os


# Define a function to determine if a file is a supported media type
def is_supported_media(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    supported_types = ['video/mp4', 'video/avi', 'video/quicktime', 'video/webm',
                       'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/aac']
    return mime_type in supported_types


# Define a function to transcode media using FFmpeg
def transcode_media(file_path, output_path):
    try:
        # Construct the FFmpeg command based on the file type
        mime_type, _ = mimetypes.guess_type(file_path)
        if 'video' in mime_type:
            cmd = ['ffmpeg', '-i', file_path, '-vcodec', 'libx264', '-crf', '23', output_path]
        elif 'audio' in mime_type:
            cmd = ['ffmpeg', '-i', file_path, '-acodec', 'libmp3lame', output_path]
        else:
            raise ValueError("Unsupported media type for transcoding")

        # Run the FFmpeg command using subprocess
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f"FFmpeg process failed with return code {e.returncode}")
    except Exception as e:
        raise Exception(f"An error occurred during transcoding: {e}")


# Pyramid view function to handle transcoding requests
@view_config(route_name='transcode', renderer='json')
def transcode(request):
    # Get the file path from the request
    file_path = request.matchdict['file_path']
    output_path = request.matchdict['output_path']

    # Check if the file is a supported media type
    if not is_supported_media(file_path):
        return {'error': 'Unsupported media type'}

    # Attempt to transcode the media
    try:
        transcode_media(file_path, output_path)
        return {'success': f'Media transcoded successfully to {output_path}'}
    except Exception as e:
        return {'error': str(e)}


# Pyramid configuration function
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.add_route('transcode', '/transcode/{file_path}/{output_path}')
        config.scan()

# Run the Pyramid application if this script is executed directly
if __name__ == '__main__':
    main({})