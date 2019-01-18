for i in *.png; do mogrify -quality 70 -resize 1000x1000\> "$i"; done
