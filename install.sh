#!/bin/sh

# Download bikeshare archive from udacity
curl -o temp.zip -L 'https://video.udacity-data.com/topher/2018/March/5aab379c_bikeshare-2/bikeshare-2.zip'

# Unzip only the relevant .csv files from the archive
unzip temp.zip chicago.csv new_york_city.csv washington.csv

# Delete the archive when finished
rm temp.zip

# Notify user that files have been downloaded
