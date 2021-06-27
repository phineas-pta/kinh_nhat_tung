# must use Ruby v2 for jekyll version < 4
FROM ruby:2-alpine

# missing tools
RUN apk add --no-cache build-base gcc cmake nodejs
RUN gem update
RUN gem install bundler

# working dir
COPY . /srv/jekyll/
WORKDIR /srv/jekyll
VOLUME /srv/jekyll

RUN bundle install

# default jekyll port
EXPOSE 4000

# must change host
CMD ["bundle", "exec", "jekyll", "serve", "--no-watch", "--host", "0.0.0.0"]
