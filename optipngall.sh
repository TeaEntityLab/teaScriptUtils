for i in *.png; do optipng -o5 -quiet -keep -preserve -dir optimized "$i"; done
