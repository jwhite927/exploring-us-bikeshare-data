#!/bin/sh

curl -o temp.zip -L 'https://video.udacity-data.com/topher/2018/March/5aab379c_bikeshare-2/bikeshare-2.zip'
unzip temp.zip chicago.csv new_york_city.csv washington.csv
rm temp.zip

