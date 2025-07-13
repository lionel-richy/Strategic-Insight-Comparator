
calculate_consensus <- function(data) {
  if (nrow(data) == 0) return(0)
  mean(data$strategic_score, na.rm = TRUE)
}
