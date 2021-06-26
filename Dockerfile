FROM ruby:alpine

RUN apk add --no-cache build-base gcc cmake nodejs
RUN gem install bundler

COPY . /srv/jekyll/
WORKDIR /srv/jekyll
VOLUME /srv/jekyll

RUN bundle install

EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--no-watch", "-H", "0.0.0.0", "-P", "4000"]
