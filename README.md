# What The Birds Say

I had this idea while I was half awake listening to a crow caw loudly at 6am into my bedroom window:

I would install a microphone outside my window that listened for bird sounds, which I could then feed into a script that identifies the bird, performs "sentiment analysis" on the bird call, and then tweets out translations of what my birds were saying to the world, so others could also benefit from what these birds have to say at 6 in the morning.

I then fell back to sleep, and dreamed of a world where this Twitter account existed.

# The Research

Predictably, there are enough research papers out there on automatic bird classification from audio recordings that I can stand on the shoulders of giants with this one. I found a competition looking for the best algorithm for tagging species of birds, picked one of the winning papers, and replicated their results. [link here...] Happily, because I'm in California, I could safely cut down on the generality of the algorithm and train only on birds that were meant to be in North America. This should make the results more reliably for my locale.

Also predictably, 'sentiment analysis' isn't as easily done on bird calls as it is on human language, but with some manual tagging effort and some creative license, something can be put together to at least immitate a sentiment analysis for my purpose.

