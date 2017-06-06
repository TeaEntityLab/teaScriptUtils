rm test.html
rm *.png

echo '<link rel="stylesheet" href="https://unpkg.com/purecss@1.0.0/build/pure-min.css" integrity="sha384-nn4HPE8lTHyVtfCBi5yW9d20FjT8BJwUXyWZT9InLYax14RDjBj46LmSztkmNP9w" crossorigin="anonymous">' >> test.html

while read p; do
  rm 0.svg
  echo '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%" viewBox="0 0 1200 628">' >> 0.svg
  echo '<defs>' >> 0.svg
  echo '<style>' >> 0.svg
  echo '.cls-1 {' >> 0.svg
  echo 'font-size: 62px;' >> 0.svg
  echo 'fill: #000;' >> 0.svg
  echo 'text-anchor: middle;' >> 0.svg
  echo "font-family: $p;" >> 0.svg
  echo '}' >> 0.svg
  echo '</style>' >> 0.svg
  echo '</defs>' >> 0.svg
  echo '<text id="name" class="cls-1" x="278" y="561">陳白翰</text>' >> 0.svg
  echo '</svg>' >> 0.svg

  inkscape -e "$p.png" 0.svg

  echo '<div class="pure-g">' >> test.html

  echo '<div class="pure-u-1-2">' >> test.html
  echo "字型名稱: $p" >> test.html
  echo '</div>' >> test.html

  echo '<div class="pure-u-1-2">' >> test.html
  echo "<img src='$p.png' class='pure-img' /><br/>" >> test.html
  echo '</div>' >> test.html

  echo '</div>' >> test.html
done <list.txt
