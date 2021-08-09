###############################################################################################################
###############################################################################################################
# XFyun Transcription
# You can find the API documentation for the transcription in the following website
# Source: https://www.xfyun.cn/services/lfasr
# Notice: Using the ID card of mainland of China to register
# Here to download the demo
# Source: https://xfyun-doc.cn-bj.ufileos.com/1564736425808301/weblfasr_python3_demo.zip
###############################################################################################################
###############################################################################################################


from moviepy.editor import VideoFileClip as clip
from weblfasr_python3_demo import RequestApi
from utilities.CONFIG import XFYUN


def extract_audio(video_path, output_path):
    """
    extract audio of a video and feed into transcription API
    """
    print('Generate audio')
    video = clip(video_path)
    audio = video.audio
    audio.write_audiofile(output_path)
    print(f'Audio stored in {output_path}.')


def time_convert(time):
    p0 = str(time % 1000)
    p0 = '0' * (3 - len(p0)) + p0
    time //= 1000
    p1 = str(time % 60)
    p1 = '0' * (2 - len(p1)) + p1
    time //= 60
    p2 = str(time % 60)
    p2 = '0' * (2 - len(p2)) + p2
    time //= 60
    p3 = str(time % 60)
    p3 = '0' * (2 - len(p3)) + p3
    return f'{p3}:{p2}:{p1},{p0}'


def generate_src(transcript, transcript_path):
    """
    convert the json style transcription str to the format
    that .srt file requires, then write into a .srt which
    have the same name with the video.
    """
    f = open(transcript_path, 'w')
    for x, y in enumerate(transcript):
        begin = time_convert(int(y['bg']))
        end = time_convert(int(y['ed']))
        script = y['onebest']
        content = f'{x+1}\n{begin} --> {end}\n{script}\n\n'
        f.write(content)
    f.close()
    print(f'Transcript stored in {transcript_path}.')


def generate(video_path):
    import os # windows
    audio_path = video_path.split('.')[0] + '.mp3'
    extract_audio(video_path, audio_path)
    api = RequestApi(appid=XFYUN.APPID, secret_key=XFYUN.SecretKey, upload_file_path=audio_path)
    transcript = api.all_api_request()
    transcript_path = video_path.split('.')[0] + '.srt'
    os.system(f'del {audio_path}')
    print(f'Delete audio {audio_path}.')
    generate_src(transcript, transcript_path)

