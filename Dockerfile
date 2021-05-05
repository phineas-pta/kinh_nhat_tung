FROM jekyll/minimal:pages

RUN apk update && apk add ruby-dev gcc make curl build-base libc-dev libffi-dev zlib-dev libxml2-dev libgcrypt-dev libxslt-dev python

RUN bundle config build.nokogiri --use-system-libraries && bundle install

EXPOSE 4000

CMD bundle exec jekyll serve --no-watch -H 0.0.0.0 -P 4000
