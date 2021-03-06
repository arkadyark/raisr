# CSC384 Final Project - Real-time Artificially Intelligent Ski Racer (RAISR)
*Mikhal and Arkady Arkhangorodsky*

Ski racing is difficult! Aside from the physical challenge, choosing an optimal path through the gates that minimizes the time to get down the hill is nontrivial. Sometimes you would want to choose a locally suboptimal path to set up better for a future gate and dump less speed. Or so the ski coaches would have you believe. Either way we want to verify this with AI!

This idea was conceived on a chairlift while skiing, to date the only scenario discovered to be more conducive to coming up with ideas than showers.

## Results

It worked!

![dope](plots/dope.gif)

## Running

pygame and Python 3 are required (tested on CDF computers). Also needs a screen to run, so if connecting to CDF over SSH, `run ssh -X`. To run the search and display the solutions in the visualizer, use:

```
python3 visualizer.py
```

Once the search completes, click on the pygame window to start.
