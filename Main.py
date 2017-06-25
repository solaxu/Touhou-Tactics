from Game import *


if __name__ == '__main__':

    Prototype_Game = CGameApp.get_instance()
    Prototype_Game.create()
    Prototype_Game.loop()
