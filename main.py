import argparse


def main():
    argparser = argparse.ArgumentParser(prog='Color based object tracking')
    argparser.add_argument('--camera', default=0,
                           type=camera_type, help="Specifies the camera source")
    argparser.add_argument(
        '--color', default=["red"], nargs='+', help="Specifies the color(s) to be detected")
    args = argparser.parse_args()
    cam_src = args.camera
    color = set(args.color)  # convert the input into set to avoid duplication
    try:
        print("Running color based object tracking task...\n"
              "Press 'q' to exit")
        track_object(cam_src, color)
    except RuntimeError as e:
        print(f"[ERROR]RuntimeError: {e}")
    except ValueError as e:
        print(f"[ERROR]ValueError: {e}")
    except Exception as e:
        print(f"[ERROR]Unexpected Error: {e}")
    finally:
        print("Task has been terminated")


if __name__ == "__main__":
    main()
