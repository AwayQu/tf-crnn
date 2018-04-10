file_b=""

i=0

for ((i=1;i<=30;i++))
   b=$(($i%25))
   file_a="${b}.PNG"
   file_b="${i}.PNG"
   cp $file_a $file_b
done

#for file_a in `ls ./*.png`; do
#
#
#    i=$(($i+1))
#    file_b="${i}.png"
#    mv $file_a $file_b
#done