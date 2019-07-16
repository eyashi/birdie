# How this will work

## The Hardware

- Maybe take apart the Alexa and use the microphones that are already inside of that. Will require figuring out which pins of the
ribbon connector do what, and how to read that audio out... shouldn't be a terribly difficult task.
- Alternatively just buy your own microphone, I'm liking the solid state devices that are in the Alexa for this job.
- Feed into a Raspberry Pi Zero W or Regular ol Raspberry Pi connected to the internet.

## The Software

- Record 10 second audio chunks continuously (until some threshold is reached for bird sounds)
- Check if there are any bird sounds in the audio.
    - If there are, save the clip.
    - If there aren't, delete that clip.
- Run bird sound clips through classifier to determine what bird said it.
- Run bird sound with additional info through classifier to determine why the bird said what it said.
