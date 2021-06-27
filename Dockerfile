FROM ruby:alpine

# missing tools
RUN apk add --no-cache build-base gcc cmake nodejs
RUN gem install bundler

# working dir
COPY . /srv/jekyll/
WORKDIR /srv/jekyll
VOLUME /srv/jekyll

RUN bundle install

# default jekyll port
EXPOSE 4000

CMD ["bundle", "exec", "jekyll", "serve", "--no-watch", "--baseurl", "''"]
