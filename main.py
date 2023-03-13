import json
import math
import os
import pprint
import subprocess
import sys
from typing import List


def run_command(params: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(params, capture_output=True)


def get_video_duration(filename: str) -> float:
    # ffprobe -v error -show_entries stream=duration -print_format json Best\ Kittycat\ Song\ \[OFFICIAL\]\ feat.\ GRUMPY\ CAT.mp4
    ret = run_command(['ffprobe', '-v', 'error', '-show_entries', 'stream=duration', '-print_format', 'json',
                       filename])
    json_data = json.loads(ret.stdout)

    max_duration = 0.0
    for stream in json_data['streams']:
        cur_duration = float(stream['duration'])
        if cur_duration > max_duration:
            max_duration = cur_duration

    return max_duration


def generate_10hrs_video(src_filename: str) -> None:
    target_duration_sec = 10 * 60 * 60
    src_duration = get_video_duration(src_filename)
    loop_count = math.ceil(target_duration_sec / src_duration)

    # ffmpeg -stream_loop 60 -i Best\ Kittycat\ Song\ \[OFFICIAL\]\ feat.\ GRUMPY\ CAT.mp4 -c copy Best\ Kittycat\ Song\ \[OFFICIAL\]\ feat.\ GRUMPY\ CAT\ 1\ hour.mp4
    splitted_filename = os.path.splitext(src_filename)
    src_base_filename = splitted_filename[0]
    src_ext = splitted_filename[1]
    run_command(['ffmpeg', '-stream_loop', str(loop_count), '-i', src_filename, '-c', 'copy', '-y',
                 f'{src_base_filename} 10 hours{src_ext}'])


def main(src_filename: str) -> None:
    generate_10hrs_video(src_filename)


if __name__ == '__main__':
    src_filename = sys.argv[1]
    main(src_filename)
