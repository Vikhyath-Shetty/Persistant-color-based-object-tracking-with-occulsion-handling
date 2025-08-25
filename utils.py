
def camera_type(cam_src: str):
    try:
        return int(cam_src)
    except ValueError as e:
        return cam_src
