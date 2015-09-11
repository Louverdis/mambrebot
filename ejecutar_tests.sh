#!/bin/sh

# Ejecutar pruebas unitarias

py.test -v

OUT=$?

if [ $OUT -eq 0 ];then
    exit 0
fi

exit 1