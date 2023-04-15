import subprocess


def run_gentle_script_writer(vid_dir_pattern):
    command = [
        "python3",
        "text_to_video/lazykh/gentleScriptWriter.py",
        "--input_file",
        vid_dir_pattern,
    ]
    subprocess.run(command, check=True)


def run_frame_drawer(
    vid_dir_pattern, use_billboards="F", jiggly_transitions="F"
) -> None:
    command = [
        "python3",
        "text_to_video/lazykh/videoDrawer.py",
        "--input_file",
        vid_dir_pattern,
        "--use_billboards",
        use_billboards,
        "--jiggly_transitions",
        jiggly_transitions,
    ]
    subprocess.run(command)


def run_gentle_aligner(vid_dir_pattern):
    input_audio = vid_dir_pattern + ".wav"
    input_text = vid_dir_pattern + "_g.txt"
    output_json = vid_dir_pattern + ".json"
    command = [
        "python3",
        "/gentle/align.py",
        input_audio,
        input_text,
        "-o",
        output_json,
    ]
    subprocess.run(command, check=True)


def run_scheduler(vid_dir_pattern):
    command = [
        "python3",
        "text_to_video/lazykh/scheduler.py",
        "--input_file",
        vid_dir_pattern,
    ]
    subprocess.run(command)


def run_ffmpeg(vid_dir_pattern, keep_frames="F"):
    command = [
        "python3",
        "text_to_video/lazykh/videoFinisher.py",
        "--input_file",
        vid_dir_pattern,
        "--keep_frames",
        keep_frames,
    ]
    subprocess.run(command)


if __name__ == "__main__":
    run_gentle_script_writer("exampleVideo/ev")
    run_gentle_aligner(
        "exampleVideo/ev.wav",
        "exampleVideo/ev_g.txt",
        "exampleVideo/ev.json",
    )
    run_scheduler("exampleVideo/ev")
    run_frame_drawer("exampleVideo/ev", "F", "F")
    run_ffmpeg("exampleVideo/ev", "F")
