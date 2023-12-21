#' UI:
#' - Genre
#' - Niveau hardloper
#' - Aantal minuten voor ieder interval: warming up; intensity; cooling down
#' - Lyrics via speechiness

#' TODO:
#' - Genre eruithalen
#' - Mapje Drive (literature review) koppelen aan Spotify features
#' - Analyseren / Model -> en grafieken opslaan en doorsturen
#' - UI maken

#' Notes meeting:
#' Personal features:
#' - heart-rate
#' - personal taste: genre
#' Musical features:
#' - BPM, LUFS afhankelijk: warming-up -> running -> cooling down
#' - Rhytme: consistent
#'


# Setup
library(tidyverse)
library(shiny)

theme_set(theme_minimal())


# Import the dataset
df <- 
  read_csv("data/spotify_data.csv") %>% 
  mutate(
    across(c(key, mode, time_signature, playlist_total_tracks), as.integer),
    duration_ms = duration_ms / 60000
  ) %>%
  rename(duration = duration_ms)


# Density plot for all numeric variables with unit intervals
other_intervals <- c("loudness", "tempo" ,"duration")
df %>%
  select_if(is.double) %>%
  pivot_longer(cols = everything()) %>%
  filter(!(name %in% other_intervals)) %>%
  ggplot(aes(x = value)) +
  geom_density() +
  scale_x_continuous(limits = c(0,1)) +
  facet_wrap(~ name, scales = "free") +
  theme(
    axis.title.x = element_blank(),
    axis.title.y = element_blank(),
    axis.text.y = element_blank()
  )

df %>%
  select(where(is.double || contains("playlist_owner"))) %>%
  pivot_longer(cols = everything()) %>%
  filter(!(name %in% other_intervals)) %>%
  ggplot(aes(x = value)) +
  geom_density() +
  scale_x_continuous(limits = c(0,1)) +
  facet_wrap(~ name, scales = "free") +
  theme(
    axis.title.x = element_blank(),
    axis.title.y = element_blank(),
    axis.text.y = element_blank()
  )


# Density plot for all numeric variables with non-unit intervals
df %>%
  select_if(is.double) %>%
  pivot_longer(cols = everything()) %>%
  filter(name %in% other_intervals) %>%
  ggplot(aes(x = value)) +
  geom_density() +
  facet_wrap(~ name, scales = "free") +
  theme(
    axis.title.x = element_blank(),
    axis.title.y = element_blank(),
    axis.text.y = element_blank()
  )

# Bar chart for all integer variables
df %>%
  select_if(is.integer) %>%
  pivot_longer(cols = everything()) %>%
  ggplot(aes(x = value)) +
  geom_bar() +
  facet_wrap(~ name, scales = "free")

plot_density <- function(col) {
  df %>%
    ggplot(aes(x = {{ col }})) +
    geom_density() +
    theme(
      axis.title.x = element_blank(),
      axis.title.y = element_blank(),
      axis.text.y = element_blank()
    ) +
    labs(title = "")  
}

