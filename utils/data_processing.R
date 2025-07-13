
load_and_process_data <- function(file_path) {
  df <- read.csv(file_path)
  df$date <- as.Date(df$date)
  return(df)
}
