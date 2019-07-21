# How this will work

- Record 10 second audio chunks continuously (until some threshold is reached for number of clips to evaluate)
- Check if there are any bird sounds in the audio.
  - If there are, save the clip & queue it for classifying.
  - If there aren't, delete that clip.
- Run bird sound clips through classifier to determine what bird said it.
- Run bird sound with additional info through classifier to determine why the bird said what it said.
  - This is the only part that really doesn't have precidence in literature. It's going to be fairly simplistic and maybe even a little make belief, but I think that will only make it funnier. Probably the least scientifically relevant part of this.

## Check if there are any bird sounds in the audio

## Classify the bird sound

## Make belief sentiment analysis on the bird sound
