FROM jekyll/minimal:pages

EXPOSE 4000

CMD bundle exec jekyll serve --no-watch -H 0.0.0.0 -P 4000
