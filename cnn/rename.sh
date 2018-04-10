file_b=""


for ((i=1;i<100;i++));
do
   b=$(( $i % 25))
   echo $b
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