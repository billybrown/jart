import RPi.GPIO as GPIO
import time
import pygame

BTN_PIN = 16
LED_PIN = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

GPIO.setup(LED_PIN, GPIO.OUT)

GPIO.output(LED_PIN, GPIO.LOW)

pygame.mixer.init()
pygame.mixer.music.load("/usr/share/scratch/Media/Sounds/Music Loops/Eggs.mp3")


is_playing = False

# button is pressed action
def playAudio(channel) :

    global is_playing

    # led action
    GPIO.output(LED_PIN, GPIO.HIGH)

    # restart audio
    if (is_playing) :
    	print("fading out music")
        pygame.mixer.music.fadeout(2000)
        time.sleep(5)
        print("restarting music.")
        pygame.mixer.music.rewind()

    # play our audio
    print("music is starting.")
    pygame.mixer.music.play()
    is_playing = True
    time.sleep(1)

# waiting around for button press
GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, callback=playAudio, bouncetime=2500)
pygame.mixer.music.set_endevent(pygame.USEREVENT)

print("JART has begun!!! INITIATE JART.")

try :
    while True :
        if (is_playing and not pygame.mixer.music.get_busy()):
            is_playing = False
            print("song has finished")
            # turn off light (start blinking)
            GPIO.output(LED_PIN, GPIO.LOW) 
except :
    pass

pygame.mixer.quit()

GPIO.cleanup()

print("done")
