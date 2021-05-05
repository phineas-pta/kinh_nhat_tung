FROM jekyll/minimal:pages

COPY --chown=jekyll:jekyll Gemfile* /site

WORKDIR /site

RUN apk update && apk add ruby-dev gcc make curl build-base libc-dev libffi-dev zlib-dev libxml2-dev libgcrypt-dev libxslt-dev python

RUN bundle config build.nokogiri --use-system-libraries && bundle install

EXPOSE 4000
