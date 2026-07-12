#!/usr/bin/env bash
# Rebuild the print PDF (6x9), EPUB, and wrap cover from the manuscript. Run from book/.
set -e
# Print sources: strip the book emoji (unrenderable in print fonts -> KDP margin errors)
rm -rf build/printsrc && mkdir -p build/printsrc
for f in chapters/*.md; do sed 's/📖 //g; s/📖//g' "$f" > "build/printsrc/$(basename $f)"; done
pandoc build/printsrc/00-front-matter.md -o build/frontmatter.html
BODY="build/printsrc/00b-introduction.md $(ls build/printsrc/ch0[1-8]*.md | sort) build/printsrc/interlude-part2-jones-carpenter.md $(ls build/printsrc/ch[0-9]*.md | sort -V | grep -v 'ch0[1-8]') build/printsrc/zz-backmatter.md"
pandoc $BODY --pdf-engine=weasyprint --css=build/book.css --toc --toc-depth=1 \
  --include-before-body=build/frontmatter.html \
  -o "build/How Not to Get Away With Murder - Interior 6x9.pdf"
rm -f build/frontmatter.html
# EPUB keeps the emoji (fine on screens) and embeds the cover
EBODY="chapters/00-front-matter.md chapters/00b-introduction.md $(ls chapters/ch0[1-8]*.md | sort) chapters/interlude-part2-jones-carpenter.md $(ls chapters/ch[0-9]*.md | sort -V | grep -v 'ch0[1-8]') chapters/zz-backmatter.md"
pandoc $EBODY -o "build/How Not to Get Away With Murder.epub" --toc --split-level=1 \
  --epub-cover-image="cover/how-not-to-get-away-with-murder-cover.jpg" \
  --metadata title="How Not to Get Away With Murder" \
  --metadata subtitle="True Stories of the Evidence That Caught Them" \
  --metadata author="Frank Alfano" --metadata lang=en-US --metadata date=2026
# Wrap cover (uses cover/author-photo.jpg in the bio block if present)
python3 build/make_cover.py
cp build/cover-wrap-6x9-196pp-WHITE.pdf cover/cover-wrap-6x9-196pp-WHITE.pdf
echo "Built interior PDF, EPUB, and wrap cover. Verify page count stays 196 or regenerate the cover spine."
