#!/usr/bin/env bash
# Rebuild the print PDF (6x9) and EPUB from the manuscript. Run from book/.
set -e
pandoc chapters/00-front-matter.md -o build/frontmatter.html
BODY="chapters/00b-introduction.md $(ls chapters/ch0[1-8]*.md | sort) chapters/interlude-part2-jones-carpenter.md $(ls chapters/ch[0-9]*.md | sort -V | grep -v 'ch0[1-8]') chapters/zz-backmatter.md"
pandoc $BODY --pdf-engine=weasyprint --css=build/book.css --toc --toc-depth=1 \
  --include-before-body=build/frontmatter.html \
  -o "build/How Not to Get Away With Murder - Interior 6x9.pdf"
EBODY="chapters/00-front-matter.md $BODY"
pandoc $EBODY -o "build/How Not to Get Away With Murder.epub" --toc --split-level=1 \
  --metadata title="How Not to Get Away With Murder" \
  --metadata subtitle="True Stories of the Evidence That Caught Them" \
  --metadata author="Frank Alfano" --metadata lang=en-US --epub-cover-image="cover/how-not-to-get-away-with-murder-cover.jpg" --metadata date=2026
rm -f build/frontmatter.html
echo "Built PDF + EPUB in build/"
