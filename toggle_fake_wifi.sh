PINGFILE=ping/phone
if [ -f "$PINGFILE" ]
then
    rm $PINGFILE
    echo "Fake wifi disabled"
else
    touch $PINGFILE
    echo "Fake wifi enabled"
fi
