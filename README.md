# What The Birds Say

I had this idea while I was half awake listening to a crow caw loudly at 6am into my bedroom:

I would install a microphone outside my window that would listen for bird sounds, which I could then feed into a script that identifies the bird, performs "sentiment analysis" on the bird call, and tweets out translations of what my birds are saying to the world... such that others could benefit from what these birds have to say at 6 in the morning.

I then fell back to sleep, and dreamed of a world where this Twitter account existed.

# The Research

Predictably, there are enough research papers out there on automatic bird classification from audio recordings that I can stand on the shoulders of giants with this one. I found a competition looking for the best algorithm for tagging audio segments for the presence of birds, [picked one of the winning papers, and attempted to replicate their results.](http://machine-listening.eecs.qmul.ac.uk/wp-content/uploads/sites/26/2017/01/cakir.pdf)

Also predictably, 'sentiment analysis' isn't as easily done on bird calls as it is on human language, but with some manual tagging effort and some creative license, something can be put together to at least immitate a sentiment analysis for my purpose (the design of something that extrapolates meaning on top of things systematically I think is still a pretty interesting topic).

So far:

1. A basic learning model (CNN) is achieving 88% accuracy in detecting clips with birds in them. I followed some results from [this challenge to make this happen.](http://machine-listening.eecs.qmul.ac.uk/bird-audio-detection-challenge/) This can be found in the 'lrn' directory.
   - More work on this model is yet to come. I think it can be better, and I definitely am not even close to the competition winners in terms of effectiveness.
2. A basic recording script has been written to facilitate gathering samples of my own (recorder.py).

To come:

1. Actually identifying the birds in my back yard!
   - Will require another model trained on another dataset, this time with tags on what kind of bird it is. Will try to get some data set local to California if possible.
2. Constructing the basis for sentiment analysis on these bird calls. This could be a laughable effort but I like to laugh.
3. Twitter integration (the easy part).
