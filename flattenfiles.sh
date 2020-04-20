shopt -s extglob
shopt -s globstar
shopt -s nullglob
tree . 

dirs=( */ ) 
for f in **/*.*
do
    dir="${f%.*}"
    mkdir -p "$dir"
    mv "$f" "$dir"
done

tree .

i=0 
for d in **/
do
    files=("$d"/*.*)
    [[ ${#files[@]} -eq 0 ]] && continue
    (( ++i ))
    for f in "${files[@]}"
    do
        mv -v "$f" $i-${f##*/}
    done
done
#rm -r */
#tree .

find ./ -type f -exec mv {} ./ \;
