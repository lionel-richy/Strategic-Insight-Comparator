
create_priority_matrix_plot <- function(data) {
  plot_ly(data, x = ~market_opportunity, y = ~competitive_impact, 
          text = ~title, type = 'scatter', mode = 'markers', 
          color = ~strategic_score, size = ~strategic_score)
}
