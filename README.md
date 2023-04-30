# ffmpeg-Compress-Video-Script
mp4파일의 용량을 줄여주는 ffmpeg명령어를 실행해주는 프로그램  
720p 해상도의 mp4영상으로 압축됩니다.


# 사용법
1. 프로그램과 같은 폴더에 'ffmpeg.exe' 파일을 둔다.
2. 프로그램과 같은 폴더에 압축할 mp4 파일들 둔다.
3. 이 프로그램을 실행시킨다.

# 실제 실행되는 명령어
```shell
ffmpeg -i "filename" -vf scale=[720p의 해상도값] -c:v libx264 -preset fast -crf 28 -pix_fmt yuv420p -c:a copy "filename_720p28.mp4"
```
