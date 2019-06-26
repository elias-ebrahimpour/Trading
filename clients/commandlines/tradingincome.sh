#!/bin/bash

source config.sh


print_usage()
{
  echo "Use this script to submit income reports tp ${BASE_URL}"
  echo "Usage: ${0} <Amount> <Description>. Eg:"
  echo "Usage: ${0} 1000 Donation"
}

AMOUNT=$1
shift
TEXT=$*
if [ -z "$TEXT" ] ; then
  print_usage
fi

curl --data "token=$TOKEN&amount=$AMOUNT&text=$TEXT" $BASE_URL/submit/income/
