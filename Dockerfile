# lightweight image
FROM ruby:alpine

# missing tools
RUN apk add --no-cache build-base gcc cmake nodejs \
 && gem update \
 && gem install bundler

# working dir
COPY . /srv/jekyll/
WORKDIR /srv/jekyll

RUN bundle install

# default jekyll port
EXPOSE 4000

# must change host
CMD ["bundle", "exec", "jekyll", "serve", "--no-watch", "--host", "0.0.0.0"]
