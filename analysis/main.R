library(tidyverse)
library(RSQLite)
library(DBI)

# Connect to database
con <- dbConnect(SQLite(), "../music.sqlite")

df <- con %>%
  dbReadTable("songs") %>%
  as_tibble()

df