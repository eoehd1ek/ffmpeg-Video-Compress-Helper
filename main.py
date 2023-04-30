import cv2
import os
from multiprocessing import *
from typing import Tuple


process_size = 4
video_extension = "mp4"
target_resolution = 720


def execute_command(queue):
    while (not queue.empty()):
        command = queue.get()
        os.system(command)


def get_resolution(path: str) -> Tuple[int, int]:
    capture = cv2.VideoCapture(path)
    if not capture.isOpened():
        print(f"could not open : {path}")
        return 0, 0

    # length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    # fps = capture.get(cv2.CAP_PROP_FPS)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height


def get_press_resolution_option(path: str) -> str:
    width, height = get_resolution(path)
    if (width == 0 and height == 0):
        return ""
    min_resolution = min(width, height)
    if (min_resolution <= target_resolution):
        return ""

    press_ratio = target_resolution / min_resolution
    result = f"-vf scale={round(width*press_ratio)}x{round(height*press_ratio)}"
    return result


def is_video_file(path: str) -> bool:
    return path[-len(video_extension):] == video_extension


def get_video_file_list() -> list[str]:
    file_list = os.listdir(os.getcwd())
    video_file_list = list(filter(is_video_file, file_list))
    return video_file_list


def get_result_file_path(path: str) -> str:
    return f"{path[:(len(path) - (len(video_extension) + 1))]}_720p28.mp4"


def get_ffmpeg_command(path: str) -> str:
    return f"ffmpeg -i \"{path}\" {get_press_resolution_option(path)} -c:v libx264 -preset fast -crf 28 -pix_fmt yuv420p -c:a copy \"{get_result_file_path(path)}\""


def main():
    freeze_support()
    command_queue = Queue()
    commands = list(map(get_ffmpeg_command, get_video_file_list()))
    for command in commands:
        command_queue.put(command)

    if (not command_queue.empty()):
        procs = []
        for _ in range(process_size):
            p = Process(target=execute_command, args=(command_queue,))
            procs.append(p)
            p.start()
        for proc in procs:
            proc.join()
        print("모든 프로세스가 join 되었습니다.(작업이 완료되었습니다.)")
    else:
        print("변경할 mp4 확장자 파일을 찾지 못했습니다.")
    os.system("pause")


if __name__ == "__main__":
    main()
