# 2016 Rap Network Analysis

This repo contains the source code and data I used to write this Medium post: https://medium.com/@paarikan/rap-connections-in-2016-59aadf9cc29d#.17qelcvli.

*scripts/billboard_rap_chart_albums.py* scrapes the Billboard rap album chart's website for 2016 and writes the results to *data/billboard_rap_chart_albums.csv*.

*scripts/find_edges.py* queries the Spotify API to find all tracks and artists for the albums, finds the number of times each pair of artists were on the same track, and then writes the weighted edges of the network to *data/artist_pair_counts.csv*.
