#  M A K E T I M E C L U B        o
#  N E W   O R L E A N S         /\
#                               /::\
#                 \ /          /::::\
#                ,a_a         /\::::/\
#               {/ ''\_      /\ \::/\ \
#               {\ ,_oo)    /\ \ \/\ \ \
#               {/  (_^____/  \ \ \ \ \ \
#     .=.      {/ \___)))*)    \ \ \ \ \/
#    (.=.`\   {/   /=;  ~/      \ \ \ \/
#        \ `\{/(   \/\  /        \ \ \/
#         \  `. `\  ) )           \ \/
#     jgs  \    // /_/_            \/
#           '==''---))))

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
audio_file_path = "jart_audio_2.mp3"
pygame.mixer.init()
pygame.mixer.music.load(audio_file_path)
pygame.mixer.music.set_volume(1.0)
os.system('amixer sset PCM,0 100%')

is_playing = False
led_brightness = 0
led_fade_step = 1
led_fade_dir = 1

# button is pressed action
# when button is pressed while the audio is already playing the volume fades out, 
# the audio rewinds to the beginning and replays,
# then the volume comes back in (it doesnt fade, it just comes back)
def playAudio(channel) :
    global is_playing

    # restart audio
    if (is_playing) :

        for volume in range(100,0,-1):
            time.sleep(0.01)
            pygame.mixer.music.set_volume(volume*.01)

        pygame.mixer.music.rewind()
        time.sleep(2)
        pygame.mixer.music.set_volume(1.0)
    else:
        pygame.mixer.music.play()
    
    is_playing = True

# fire playback event when button is pressed
GPIO.add_event_detect(BTN_PIN, GPIO.FALLING, callback=playAudio, bouncetime=2000)

# this controls the blinking LED
try :
    while True :
        if (is_playing):
            led_brightness = 100

            if (not pygame.mixer.music.get_busy()):
                is_playing = False

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
