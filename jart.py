import RPi.GPIO as GPIO
import time
import pygame
import sys, os
import subprocess

BTN_PIN = 12
LED_PIN = 16

# configure ports for button and LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)

# setup PWM for fading LED
pwm = GPIO.PWM(LED_PIN, 333)
pwm.start(0)

# load audio file
audio_file_path = "/usr/share/scratch/Media/Sounds/Vocals/Got-inspiration.mp3"
pygame.mixer.init()
pygame.mixer.music.load(audio_file_path)

playerprocess = None

is_playing = False
led_brightness = 0
led_fade_step = 1
led_fade_dir = 1

# button is pressed action
def playAudio(channel) :
    global is_playing
    
    
    
    # restart audio
    if (is_playing) :
        #print("fading out music")
        #pygame.mixer.music.fadeout(1000)
        #pygame.mixer.music.stop()
        #time.sleep(1)
        #pygame.mixer.music.pause()
        #print "sound position: {0}".format(pygame.mixer.music.get_pos())
        #pygame.mixer.music.rewind()
        #print "sound position: {0}".format(pygame.mixer.music.get_pos())
        #pygame.mixer.music.unpause()
        #print("sound is restarting.")
        #time.sleep(0.1)
        print("sound is already playing")
    else:
        # play  audio
        print("sound is starting.")
        #pygame.mixer.music.rewind()
        #time.sleep(0.1)
        pygame.mixer.music.play()
    
    
    is_playing = True
    time.sleep(1)

# fire playback event when button is pressed
GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, callback=playAudio, bouncetime=2000)

print("JART has begun!!! INITIATE JART.")

try :
#if (True):
    while True :
        if (is_playing):
            led_brightness = 100

            if (not pygame.mixer.music.get_busy()):
                is_playing = False
                print("sound is finished.")

        else:
            # when not playing, fade LED in and out
            if (led_fade_dir == 1):
                led_brightness += led_fade_step
                if (led_brightness >= 100):
                    led_brightness = 100
                    led_fade_dir = 0
            else:
                led_brightness -= led_fade_step
                if (led_brightness <= 15):
                    led_brightness = 15
                    led_fade_dir = 1

        pwm.ChangeDutyCycle(led_brightness)
        time.sleep(0.015)
 
except :
    print sys.exc_info()[0]

finally:
    pygame.mixer.quit()
    GPIO.cleanup()
    print("done")
