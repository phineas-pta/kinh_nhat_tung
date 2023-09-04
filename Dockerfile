###############################################################################

FROM ruby:latest AS build

WORKDIR /home

# install deps (docker cache)
COPY Gemfile .
RUN bundle install

# build
COPY . .
RUN bundle exec jekyll build --baseurl ''

###############################################################################

FROM python:alpine

LABEL name="Kinh nhật tụng"
LABEL description="Vietnamese Mahayana Buddhism rituals in multiple languages"
LABEL author="PTA"

WORKDIR /home

COPY --from=build /home/_site .

# default python port
EXPOSE 8000

CMD ["python", "-m", "http.server"]
