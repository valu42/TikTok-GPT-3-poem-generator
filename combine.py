import os 
import moviepy.moviepy.editor as mp
import sys

topic = sys.argv[1]
video_path = f"videos/{topic}"

grey_video = mp.VideoFileClip(f"assets/grey/grey.mp4").set_duration(1)

def create_compilation(path):
    assert(os.path.exists(path))
    clips = []
    for filename in sorted(os.listdir(path)):
        if filename.endswith(".mp4"):
            clips.append(mp.VideoFileClip(f"{path}/{filename}"))
            clips.append(grey_video)

    compilation = mp.concatenate_videoclips(clips)
    compilation.write_videofile(f"{path}/result.mp4")

create_compilation(video_path)