
# STRATEGIC INSIGHT COMPARATOR
# Application Shiny pour l'analyse comparative d'IA

# Libraries
library(shiny)
library(shinydashboard)
library(DT)
library(plotly)
library(dplyr)
library(ggplot2)
library(wordcloud2)
library(timevis)

# Source modules et fonctions
source("utils/data_processing.R")
source("utils/plotting_functions.R")
source("utils/scoring_functions.R")

# Load data
analyses_data <- load_and_process_data("data/sample_analyses.csv")

# Interface utilisateur
ui <- dashboardPage(
  dashboardHeader(title = "Strategic Insight Comparator"),
  
  dashboardSidebar(
    sidebarMenu(
      menuItem("Vue d'Ensemble", tabName = "dashboard", icon = icon("tachometer-alt")),
      menuItem("Comparaison IA", tabName = "comparison", icon = icon("balance-scale")),
      menuItem("Tendances", tabName = "trends", icon = icon("chart-line"))
    )
  ),
  
  dashboardBody(
    # CSS personnalisé
    tags$head(tags$link(rel = "stylesheet", type = "text/css", href = "custom.css")),
    
    tabItems(
      # Tab 1: Dashboard principal
      tabItem(tabName = "dashboard",
        fluidRow(
          # KPIs boxes
          valueBoxOutput("total_articles"),
          valueBoxOutput("avg_strategic_score")
        ),
        fluidRow(
          # Graphique principal
          box(title = "Matrice de Priorisation", status = "primary", solidHeader = TRUE,
              width = 8, plotlyOutput("priority_matrix")),
          # Filtres
          box(title = "Filtres", status = "warning", width = 4,
              dateRangeInput("date_range", "Période:", start = min(analyses_data$date), end = max(analyses_data$date)),
              selectInput("source_filter", "Source:", choices = c("All", unique(analyses_data$source))),
              sliderInput("min_score", "Score minimum:", min = 0, max = 10, value = 5))
        ),
        fluidRow(
          # Tableau articles
          box(title = "Articles Analysés", status = "success", solidHeader = TRUE,
              width = 12, DT::dataTableOutput("articles_table"))
        )
      ),
      
      # Tab 2: Comparaison IA
      tabItem(tabName = "comparison",
        fluidRow(
          box(title = "Sélection Article", status = "primary", width = 12,
              selectInput("selected_article", "Choisir un article:", choices = unique(analyses_data$title)))
        ),
        fluidRow(
          box(title = "Comparaison des Modèles", status = "info", width = 8,
              DT::dataTableOutput("comparison_table"))
        )
      ),
      
      # Tab 3: Tendances
      tabItem(tabName = "trends",
        fluidRow(
          box(title = "Entités Principales", status = "success", width = 12,
              wordcloud2Output("entities_wordcloud"))
        )
      )
    )
  )
)

# Logique serveur
server <- function(input, output, session) {
  
  # Données réactives
  filtered_data <- reactive({
    data <- analyses_data
    if (input$source_filter != "All") {
      data <- data[data$source == input$source_filter, ]
    }
    data <- data[data$date >= input$date_range[1] & data$date <= input$date_range[2], ]
    data <- data[data$strategic_score >= input$min_score, ]
    data
  })
  
  # Outputs pour Dashboard
  output$total_articles <- renderValueBox({
    valueBox(
      value = nrow(filtered_data()),
      subtitle = "Articles Analysés",
      icon = icon("file-text"),
      color = "blue"
    )
  })
  
  output$avg_strategic_score <- renderValueBox({
    valueBox(
      value = round(mean(filtered_data()$strategic_score), 2),
      subtitle = "Score Stratégique Moyen",
      icon = icon("chart-bar"),
      color = "green"
    )
  })
  
  output$priority_matrix <- renderPlotly({
    create_priority_matrix_plot(filtered_data())
  })
  
  output$articles_table <- DT::renderDataTable({
    DT::datatable(filtered_data(), options = list(pageLength = 5))
  })
  
  # Outputs pour Comparaison
  comparison_data <- reactive({
    analyses_data[analyses_data$title == input$selected_article, ]
  })
  
  output$comparison_table <- DT::renderDataTable({
    DT::datatable(comparison_data(), options = list(pageLength = 3))
  })
  
  # Outputs pour Tendances
  output$entities_wordcloud <- renderWordcloud2({
    text <- paste(filtered_data()$entities, collapse = " ")
    words <- unlist(strsplit(text, ","))
    word_freq <- table(words)
    wordcloud2(data.frame(word = names(word_freq), freq = as.numeric(word_freq)))
  })
}

# Lancement de l'application
shinyApp(ui = ui, server = server)
