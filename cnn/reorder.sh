file_b=""

i=0
for file_a in `ls ./*.PNG`; do
    a=$(printf "%06d" "$i")
    file_b="${a}.PNG"

    mv $file_a $file_b
    i=$(($i+1))
done
