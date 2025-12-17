#!/bin/bash

year="2025"
day="1"

while [[ $# -gt 0 ]]; do
    case "$1" in 
        --year) 
            [[ -z "$2" ]] && { echo "Error: --year requires a value"; exit 1; }
            { year="$2"; shift 2; };;
        --day) 
            [[ -z "$2" ]] && { echo "Error: --day requires a value"; exit 1; }
            { day="$2"; shift 2; };;
        *) { echo "unexpected argument $1"; exit 1; };
    esac
done

echo "Running for Year: $year and Day: $day ..."
python -m "$year.code.$day" 