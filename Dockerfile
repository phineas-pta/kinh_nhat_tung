FROM jekyll/jekyll:builder

COPY --chown=jekyll:jekyll . /srv/jekyll/

WORKDIR /srv/jekyll

RUN bundle config build.nokogiri --use-system-libraries && bundle install

EXPOSE 4000

CMD bundle exec jekyll serve -H 0.0.0.0 -P 4000
