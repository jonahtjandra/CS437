from sense_hat import SenseHat
from time import sleep

sense=SenseHat()
sense.clear()
currX = 3
currY = 5
sense.set_pixel(currX,currY,(255,255,0))
while True:
    for event in sense.stick.get_events():
        if event.action =="pressed":
         
         prevX,prevY=currX,currY
            if event.direction == "right":
                currX += 1
            elif event.direction == "left":
                currX -= 1
            elif event.direction == "up":
                currY -= 1
            elif event.direction == "down":
                currY += 1
            else:
                sense.clear()
                exit()
            if not (currX >= 0 and currY >= 0 and currX < 8 and currY < 8):
                currX,currY=prevX,prevY
            sense.set_pixel(prevX,prevY,(0,0,0))
            sense.set_pixel(currX,currY,(255,255,0))
                

        

            