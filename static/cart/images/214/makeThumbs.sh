# makeThumbs.sh 200 src/ src/x200/
height=$1; src=$2; dest=$3; \
for image in $src*; do \
    image=$(basename "$image"); \
    hasThumb=False; \
    for thumb in $dest*; do \
        thumb=$(basename "$thumb"); \
        if [[ "$image" == "$thumb" ]]; then \
            hasThumb=True; \
        fi; \
    done; \
    if [[ $hasThumb == False ]]; then \
        printf "converting:"$src$image" -> "$dest$image"\n"; \
        convert $src$image -resize x$height $dest$image; \
    fi; \
done