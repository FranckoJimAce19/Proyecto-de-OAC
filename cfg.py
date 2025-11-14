import os 
FPS = 40
SCREENSIZE = (640, 640)
SKIER_IMAGE_PATH = [
    os.path.join(os.getcwd(), "Skier/resources/images/skier_forward.png"),
    os.path.join(os.getcwd(), "Skier/resources/images/skier_right1.png"),
    os.path.join(os.getcwd(), "Skier/resources/images/skier_right2.png"),
    os.path.join(os.getcwd(), "Skier/resources/images/skier_left2.png"),
    os.path.join(os.getcwd(), "Skier/resources/images/skier_left1.png"),
    os.path.join(os.getcwd(), "Skier/resources/images/skier_fall.png")
    ]

OBSTICE_PATH = {
    "tree": os.path.join(os.getcwd(), "Skier/resources/images/tree.png"),
    "flag": os.path.join(os.getcwd(), "Skier/resources/images/flag.png")}

BMGPATH = os.path.join(os.getcwd(), "Skier/resources/music/bgm.mp3")
FONTPATH = os.path.join(os.getcwd(), "Skier/resources/font/FZSTK.TTF")

HIGHEST_SCORE_RECORD_FILEPATH = 'Skier/scores.rec'
