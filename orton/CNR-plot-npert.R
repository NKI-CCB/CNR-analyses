library(tidyverse)

# Set graphic options
use_theme <- theme(
  text = element_text(colour = "black", size = 6, family = "Helvetica"),
  # line = element_line(colour = "black", size = .3),
  title = element_text(colour = "black", size = 6, family = "Helvetica"),
  axis.title = element_text(colour = "black", size = 6, family = "Helvetica"),
  panel.grid = element_blank(),
  panel.background = element_blank(),
  # aspect.ratio = 1,
  axis.ticks.y = element_blank(),
  axis.line.x = element_line(),
  axis.line.y = element_line(),
  axis.text = element_text(colour = "black", size = 4),
  legend.text = element_text(colour = "black", size = 4, family = "Helvetica")
)

breaks <- c(
  "braf", "braf_wt_theta",
  "ras", "ras_wt_theta",
  "egfr", "egfr_wt_theta",
  "wt", "all_theta"
)

cols <- c(RColorBrewer::brewer.pal(6, "Paired"), "gray", "black")
names(cols) <- breaks

clabs <- c(
  "BRAFmut only", "BRAFmut + WT",
  "RASmut only", "RASmut + WT",
  "EGFRmut only", "EGFRmut + WT",
  "Wt only", "All lines combined"
)
names(clabs) <- breaks

# True and False postive rate ####

# Get the data
df <- read_tsv("../results/solutions/npert-tpr-fpr.tsv")
order_braf <-  c("wt", "braf", "braf_wt_theta", "all_theta")

df_use <- df %>%
  filter(cl %in% order_braf) %>%
  mutate(cl = factor(cl, levels = order_braf))

p_tpr <- ggplot(df_use, aes(x = factor(NPERT), y = tpr, color = cl)) +
  geom_boxplot(outlier.size = 0.5, position = position_dodge2(preserve = "total")) +
  scale_color_manual(values = cols, labels = clabs, breaks = breaks, name = "") +
  use_theme +
  labs(y = "True positive rate") +
  theme(
    legend.position = "None",
    axis.title.x = element_blank()
    )

p_fpr <- ggplot(df_use, aes(x = factor(NPERT), y = fpr, color = cl)) +
  geom_boxplot(outlier.size = 0.5, position = position_dodge2(preserve = "total")) +
  labs(x = "Number of perturbations", y = "False positive rate") +
  scale_color_manual(values = cols, labels = clabs, breaks = breaks, name = "") +
  use_theme +
  theme(
    legend.position = "none",
    legend.key = element_rect(fill = "transparent", colour = "transparent", size = unit(1, "line")),
    legend.key.size = unit(0.5, "line"),
    legend.margin =  margin(0, 0, 0, 0, "lines")
  ) +
  guides(color = guide_legend(ncol = 2))

myutils::multiplot(p_tpr, p_fpr)
pdf("~/Desktop/tpr-fpr-npert.pdf",
    height = 5*0.39, width = 5*0.39)
myutils::multiplot(p_tpr, p_fpr)
dev.off()


ynames <- c("True positive rate", "False positive rate")
names(ynames) <- c("tpr", "fpr")

df_all <- df %>%
  gather(rate, value, tpr, fpr) %>%
  mutate(
    rate = factor(rate, levels = c("tpr", "fpr")),
    plot_group = factor(
      case_when(
        str_detect(cl, "braf") ~ "BRAFmut",
        str_detect(cl, "ras")  ~ "RASmut",
        str_detect(cl, "egfr") ~ "EGFRmut",
        TRUE                      ~ "WT/All cell lines"
      ),
      levels = c("BRAFmut", "RASmut", "EGFRmut", "WT/All cell lines")
    )
  )

plt_all <- ggplot(df_all, aes(x = factor(NPERT), y = value, color = cl)) +
  geom_boxplot(outlier.size = 0.5, position = position_dodge2(preserve = "total")) +
  scale_color_manual(values = cols, labels = clabs, breaks = breaks, name = "") +
  labs(x = "Number of perturbations", y = "") +
  facet_grid(rate ~ plot_group, scales = "free", switch = "y",
             labeller = labeller(rate = ynames)) +
  theme(
    text = element_text(colour = "black", size = 8, family = "Helvetica"),
    axis.text.x = element_text(size = 8),
    #legend.text = element_text(colour = "black", size = 6, family = "Helvetica"),
    legend.position = "bottom"
  ) +
  guides(color = guide_legend(override.aes = list(fill = NA)))

plt_all
# ggsave("~/Dropbox/projects/cnr/manuscript/figures/supplementary-figures/npert-all.pdf",
#        plt_all, width = 13.2, height = 8, units = "cm")

rm(df, df_all, df_use, p_fpr, p_tpr, plt_all)

# Prediction of unperturbed nodes with prior network knowledge ####

## Get the data
df_prediction <- read_tsv("~/Dropbox/projects/cnr/orton/results/solutions/npert-correlations-priornetwork.tsv")
order_braf <-  c("wt", "braf", "braf_wt_theta", "all_theta")

prediction_use <- df_prediction %>%
  rename(panel = PANEL) %>%
  mutate(
    plot_group = factor(
      case_when(
        str_detect(panel, "braf") ~ "BRAFmut",
        str_detect(panel, "ras")  ~ "RASmut",
        str_detect(panel, "egfr") ~ "EGFRmut",
        TRUE                      ~ "WT/All cell lines"
      ),
      levels = c("BRAFmut", "RASmut", "EGFRmut", "WT/All cell lines")),
    panel = factor(panel, levels = breaks)
  )

prediction_braf <- prediction_use %>%
  filter(panel %in% order_braf) %>%
  mutate(panel = factor(panel, levels = order_braf))

## BRAF and WT only

plt_prediction_braf <- ggplot(prediction_braf, aes(x = factor(NPERT), y = spearmanr, color = panel)) +
  geom_boxplot(outlier.size = 0.25) +
  #ggbeeswarm::geom_quasirandom(dodge.width = , size = 0.1, position = position_dodge(width = 1)) +
  labs(
    x = "Number of perturbations",
    y = "Spearman correlation",
    title = "CNR prediction vs ODE simulation"
  ) +
  scale_color_manual(values = cols, labels = clabs[order_braf], breaks = order_braf, name = "") +
  use_theme +
  theme(
    legend.position = "left",
    legend.key = element_rect(fill = "transparent", colour = "transparent", size = unit(1, "line")),
    legend.key.size = unit(0.5, "line"),
    legend.margin =  margin(0, 0, 0, 0, "lines")
  )
plt_prediction_braf


## All panels

# Spearman
plt_prediction_all <- ggplot(prediction_use, aes(x = factor(NPERT), y = spearmanr, color = panel)) +
  geom_boxplot(outlier.size = 0.5, position = position_dodge2(preserve = "total")) +
  #ggbeeswarm::geom_quasirandom(dodge.width = 1, size = 0.1) +
  labs(
    x = "Number of perturbations",
    y = "Spearman correlation",
    title = "CNR prediction vs ODE simulation") +
  scale_color_manual(values = cols, labels = clabs, breaks = breaks, name = "") +
  theme(
    text = element_text(colour = "black", size = 8, family = "Helvetica"),
    axis.text.x = element_text(size = 8),
    #legend.text = element_text(colour = "black", size = 6, family = "Helvetica"),
    legend.position = "bottom"
  ) +
  facet_wrap(~plot_group, ncol = 4)
plt_prediction_all

# Correlation between true and fitter parameters with prior network knowledge ####

param <- read_tsv("../results/solutions/npert-correlations-param-priornetwork.tsv")

param_use <- param %>%
  rename(panel = PANEL) %>%
  mutate(
    plot_group = factor(
      case_when(
        str_detect(panel, "braf") ~ "BRAFmut",
        str_detect(panel, "ras")  ~ "RASmut",
        str_detect(panel, "egfr") ~ "EGFRmut",
        TRUE                      ~ "WT/All cell lines"
      ),
      levels = c("BRAFmut", "RASmut", "EGFRmut", "WT/All cell lines")
    ),
    panel = factor(panel, levels = breaks)
  )


param_braf <- param_use %>%
  filter(panel %in% order_braf) %>%
  mutate(panel = factor(panel, levels = order_braf))

# ggplot(param_braf, aes(x = factor(NPERT), y = pearsonr, color = panel)) +
#   geom_boxplot(outlier.size = 0.25) +
#   labs(
#     x = "Number of perturbations",
#     y = "Pearson correlation",
#     title = "True vs fitted model parameters"
#   ) +
#   scale_color_manual(values = cols, labels = clabs[order_braf], breaks = order_braf, name = "") +
#   use_theme +
#   theme(
#     legend.position = "left",
#     legend.key = element_rect(fill = "transparent", colour = "transparent", size = unit(1, "line")),
#     legend.key.size = unit(0.5, "line"),
#     legend.margin =  margin(0, 0, 0, 0, "lines")
#   )
# #ggsave("~/Dropbox/projects/cnr/manuscript/figures/subfigures/orton/param-pearson-npert.pdf",
#        height = 4, width = 7, units = "cm")

plt_param_braf <- ggplot(param_braf, aes(x = factor(NPERT), y = spearmanr, color = panel)) +
  geom_boxplot(outlier.size = 0.25) +
  labs(
    x = "Number of perturbations",
    y = "Spearman correlation",
    title = "True vs fitted model parameters"
  ) +
  scale_color_manual(values = cols, labels = clabs[order_braf], breaks = order_braf, name = "") +
  use_theme +
  theme(
    legend.position = "left",
    legend.key = element_rect(fill = "transparent", colour = "transparent", size = unit(1, "line")),
    legend.key.size = unit(0.5, "line"),
    legend.margin =  margin(0, 0, 0, 0, "lines")
  )
plt_param_braf


## All panels

plt_param_all <- ggplot(param_use, aes(x = factor(NPERT), y = spearmanr, color = panel)) +
  geom_boxplot(outlier.size = 0.5, position = position_dodge2(preserve = "total")) +
  labs(
    x = "Number of perturbations",
    y = "Spearman correlation",
    title = "True vs fitted model parameters"
    ) +
  scale_color_manual(values = cols, labels = clabs, breaks = breaks, name = "") +
  # expand_limits(y = c(-1, 1)) +
  theme(
    text = element_text(colour = "black", size = 8, family = "Helvetica"),
    axis.text.x = element_text(size = 8),
    #legend.text = element_text(colour = "black", size = 6, family = "Helvetica"),
    legend.position = "bottom"
  ) +
  facet_wrap(~plot_group, ncol = 4)

plt_param_all

