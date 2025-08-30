import argparse
import logging
from type import camera_type
from tracker import *

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    argparser = argparse.ArgumentParser(prog='Color based object tracking')
    argparser.add_argument('--camera', default=0,
                           type=camera_type, help='Specifies the camera source')
    argparser.add_argument(
        '--color', default=["red"], nargs='+', choices=['red', 'green', 'blue', 'yellow'], help="Specifies the color(s) to be detected")
    argparser.add_argument('-n', default=1, type=int,
                           help='Number of object(s) to detect at a time')
    args = argparser.parse_args()
    cam_src = args.camera
    n = args.n
    color = set(args.color)  # convert the input into set to avoid duplication
    try:
        print("Running color based object tracking task...\n"
              "Press 'q' to exit")
        tracker = ObjectTracker(cam_src,color,n)
        tracker.run()
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
