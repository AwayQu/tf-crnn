file_b=""


for ((i=1;i<5500;i++));
do
   b=$(( $i % 272))
   echo $b
   c=$(printf "%06d" "$b")
   d=$(printf "%06d" "$i")
   file_a="${c}.PNG"
   file_b="${d}.PNG"
   cp $file_a $file_b
done
#for file_a in `ls ./*.png`; do
#
#
#    i=$(($i+1))
#    file_b="${i}.png"
#    mv $file_a $file_b
#done
