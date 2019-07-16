# How this will work

## The Hardware

- Maybe take apart the Alexa and use the microphones that are already inside of that. Will require figuring out which pins of the
ribbon connector do what, and how to read that audio out... shouldn't be a terribly difficult task.
- Alternatively just buy your own microphone, I'm liking the [MEMS devices](https://www.adafruit.com/product/2716?gclid=Cj0KCQjwyLDpBRCxARIsAEENsrIX4VWxq3Evc8aPzhe1zFPCpNcolBYYhdIfaJvOkuVuHKHy2f-rPdEaAvF5EALw_wcB) that are in the Alexa for this job.
- Feed into a Raspberry Pi Zero W or Regular ol Raspberry Pi connected to the internet.

## The Software

### These are the steps required for the thing to work:
- Record 10 second audio chunks continuously (until some threshold is reached for number of clips to evaluate)
- Check if there are any bird sounds in the audio.
    - If there are, save the clip & queue it for classifying.
    - If there aren't, delete that clip.
- Run bird sound clips through classifier to determine what bird said it.
- Run bird sound with additional info through classifier to determine why the bird said what it said.
    - This is the only part that really doesn't have precidence in literature. It's going to be fairly simplistic and maybe even a little make belief, but I think that will only make it funnier. Probably the least scientifically relevant part of this.


