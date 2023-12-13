library(tidyverse)
library(RSQLite)
library(DBI)

# Connect to database
con <- dbConnect(SQLite(), "../music.sqlite")

df <- con %>%
  dbReadTable("songs") %>%
  as_tibble()

theme_set(theme_minimal())

df %>%
  ggplot(aes(x = tempo)) +
  geom_histogram()

df %>%
  ggplot(aes(x = scale)) +
  geom_bar()

df %>%
  ggplot(aes(x = key)) +
  geom_bar()
