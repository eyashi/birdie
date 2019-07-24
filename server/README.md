# Data Logging Server

There's probably a simpler architecture for this, but I'm just going to build what I know:

## A Flask server to run a dashboard and execute processing

This server will run on the host computer, listen for any requests to process an audio clip recorded, create a prediction for whether there are any bird sounds in the clip, and update the dashboard for bird counts.
