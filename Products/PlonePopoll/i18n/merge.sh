#!/bin/bash

echo "Syncing PlonePopoll domain PO files..."
for PO in PlonePopoll_??.po; do
  echo $PO
  i18ndude sync --pot PlonePopoll.pot $PO
done
echo "done."
echo ""

echo "Syncing plone domain PO files..."
for PO in PlonePopoll_plone_??.po; do
  echo $PO
  i18ndude sync --pot PlonePopoll_plone.pot $PO
done
echo "done."
