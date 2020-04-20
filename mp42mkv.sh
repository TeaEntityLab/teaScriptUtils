for i in *.mp4; do
    ffmpeg -i "$i" -codec copy "${i%.*}.mkv"
done
