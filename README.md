# convert-le-monde-epub

pandoc -f html -t epub3 --epub-metadata=metadata.xml -o output.epub input.html


pandoc -f html -t epub2 -o output.epub Modif_juste_contenu_no_comment.html

## Call pandoc via Python

https://janakiev.com/blog/python-shell-commands/