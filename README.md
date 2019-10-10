# What The Birds Say

I had this idea while I was half awake listening to a crow caw loudly at 6am into my bedroom:

I would install a microphone outside my window that would listen for bird sounds, which I could then feed into a script that identifies the bird, performs "sentiment analysis" on the bird call, and tweets out translations of what my birds are saying to the world... such that others could benefit from what these birds have to say at 6 in the morning.

I then fell back to sleep, and dreamed of a world where this Twitter account existed.

So this was a pretty whack idea, mostly a joke, but developing a low-cost ecological monitoring solution *does* sound pretty appealing, and maybe even relevant to the community.

# The Research

Predictably, there are enough research papers out there on automatic bird classification from audio recordings that I can stand on the shoulders of giants with this one. I found a competition looking for the best algorithm for tagging audio segments for the presence of birds, [picked one of the winning papers, and attempted to replicate their results.](http://machine-listening.eecs.qmul.ac.uk/wp-content/uploads/sites/26/2017/01/cakir.pdf)

So far:

1. A basic learning model (CNN) is achieving 88% accuracy in detecting clips with birds in them. I followed some results from [this challenge to make this happen.](http://machine-listening.eecs.qmul.ac.uk/bird-audio-detection-challenge/)
2. A basic recording script has been written to facilitate gathering samples of my own (recorder.py).

To come:

1. Applying labels to the bird sounds in my backyard.
   - Will require another model trained on another dataset, this time with tags on what kind of bird it is. Will try to get some dataset local to California if possible.
   - Following [these](https://www-cs.stanford.edu/~acoates/papers/coatesng_nntot2012.pdf) [papers](https://www.semanticscholar.org/paper/End-to-end-learning-for-music-audio-Dieleman-Schrauwen/e93c7d71074c0d4890915263c7c34711d41b6940) to get my model working with [unsupervised feature learning](https://peerj.com/articles/488/). This is to improve on the possibility of being able to label which birds are present in an audio clip.
2. Evaluating the domain adaptation of my model & improving on it, using many different recorders in different environments around town. First will work this out with the many different training datasets available, and when some semblance of generality is established, distributing the recording devices among curious individuals to test on new data.

# Data Logging Server

## A Flask server to run a dashboard and execute processing

This server will run on the host computer, listen for any requests to process an audio clip recorded, create a prediction for whether there are any bird sounds in the clip, and update the dashboard for bird counts.

There should also be some interface to interact with the data, improve tags, and feed back into the model.