# ----------------------------------------------------------------              
# Agibank MLOps Challenge - Training Template
# ----------------------------------------------------------------
# Objetivo: Este script serve como base para o pipeline de MLOps.
# O candidato deve containerizar e integrar este código ao pipeline.
# ----------------------------------------------------------------

library(tidymodels)
library(readr)
library(jsonlite)

cat("=== Iniciando treinamento do modelo ===\n\n")

# ----------------------------------------------------------------
# 1. CARREGAR DADOS
# ----------------------------------------------------------------

data_path <- Sys.getenv("DATA_PATH", "data/application_train.csv")
cat("Carregando dados de:", data_path, "\n")

df <- read_csv(data_path, show_col_types = FALSE) %>% 
  select(TARGET, AMT_INCOME_TOTAL, AMT_CREDIT, DAYS_BIRTH, AMT_GOODS_PRICE) %>%
  mutate(TARGET = as.factor(TARGET))

cat("Dados carregados:", nrow(df), "linhas\n\n")

# ----------------------------------------------------------------
# 2. PREPARAR MODELO
# ----------------------------------------------------------------

cat("Preparando pipeline de modelagem...\n")

model_recipe <- recipe(TARGET ~ ., data = df) %>%
  step_impute_median(all_numeric_predictors()) %>%
  step_normalize(all_numeric_predictors())

model_spec <- logistic_reg() %>%
  set_engine("glm") %>%
  set_mode("classification")

model_workflow <- workflow() %>%
  add_recipe(model_recipe) %>%
  add_model(model_spec)

# ----------------------------------------------------------------
# 3. TREINAR MODELO
# ----------------------------------------------------------------

cat("Treinando modelo...\n")
final_model <- fit(model_workflow, data = df)
cat("Treinamento concluído!\n\n")

# ----------------------------------------------------------------
# 4. SALVAR ARTEFATOS
# ----------------------------------------------------------------

output_dir <- Sys.getenv("MODEL_OUTPUT_PATH", "artifacts")
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

model_path <- file.path(output_dir, "model_v1.rds")
saveRDS(final_model, model_path)
cat("✓ Modelo salvo em:", model_path, "\n")

# Salvar metadados básicos
metadata <- list(
  version = "1.0",
  created_at = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
  features = c("AMT_INCOME_TOTAL", "AMT_CREDIT", "DAYS_BIRTH", "AMT_GOODS_PRICE")
)

metadata_path <- file.path(output_dir, "model_metadata.json")
write_json(metadata, metadata_path, pretty = TRUE, auto_unbox = TRUE)
cat("✓ Metadados salvos em:", metadata_path, "\n")

cat("\n=== Treinamento finalizado com sucesso! ===\n")