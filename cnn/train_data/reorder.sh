file_b=""

i=0
for file_a in `ls ./*.png`; do
    a=$(printf "%06d" "$i")
    file_b="${a}.png"

    mv $file_a $file_b
    i=$(($i+1))
done
