for i in *.jpg; do mogrify -strip -interlace Plane -gaussian-blur 0.05 -quality 70 -resize 1000x1000\> "$i"; done
