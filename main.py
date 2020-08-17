__author__ = 'newtonis'

import graphic
import logic
import thread

def main():
    logic.start(graphic)
    graphic.start(logic)

    while not graphic.end():
        graphic.update()
        logic.update()

if __name__ == "__main__":
    main()