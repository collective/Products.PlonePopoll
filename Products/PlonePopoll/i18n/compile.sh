#!/bin/bash
for po in $(find . -path '*.po'); do
    msgfmt -o ${po/%po/mo} $po;
done
