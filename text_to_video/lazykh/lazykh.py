import subprocess


def run_gentle_script_writer(input_file):
    command = [
        "python3",
        "text_to_video/lazykh/gentleScriptWriter.py",
        "--input_file",
        input_file,
    ]
    subprocess.run(command)


def draw_frames(input_file, use_billboards, jiggly_transitions):
    command = [
        "python3",
        "text_to_video/lazykh/videoDrawer.py",
        "--input_file",
        input_file,
        "--use_billboards",
        use_billboards,
        "--jiggly_transitions",
        jiggly_transitions,
    ]
    subprocess.run(command)


def run_gentle_align(input_audio, input_text, output_json):
    command = [
        "python3",
        "third_party/gentle/align.py",
        input_audio,
        input_text,
        "-o",
        output_json,
    ]
    subprocess.run(command)


def run_scheduler(input_file):
    command = [
        "python3",
        "text_to_video/lazykh/scheduler.py",
        "--input_file",
        input_file,
    ]
    subprocess.run(command)


def render_video(input_file, keep_frames):
    command = [
        "python3",
        "text_to_video/lazykh/videoFinisher.py",
        "--input_file",
        input_file,
        "--keep_frames",
        keep_frames,
    ]
    subprocess.run(command)


if __name__ == "__main__":
    run_gentle_script_writer("exampleVideo/ev")
    run_gentle_align(
        "exampleVideo/ev.wav",
        "exampleVideo/ev_g.txt",
        "exampleVideo/ev.json",
    )
    run_scheduler("exampleVideo/ev")
    draw_frames("exampleVideo/ev", "F", "F")
    render_video("exampleVideo/ev", "F")
