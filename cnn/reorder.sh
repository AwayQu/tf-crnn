file_b=""

i=0
for file_a in `ls ./*.PNG`; do
    file_b="${i}.PNG"
    mv $file_a $file_b
    i=$(($i+1))
done
