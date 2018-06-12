library(tidyverse)
library(scam)
library(here)
# Prepare plotting options ####

# Set graphic options
use_theme <- theme(
  text = element_text(colour = "black", size = 8, family = "Helvetica"),
  # line = element_line(colour = "black", size = .3),
  title = element_text(colour = "black", size = 8, family = "Helvetica"),
  axis.title = element_text(colour = "black", size = 8, family = "Helvetica"),
  panel.grid = element_blank(),
  panel.background = element_blank(),
  # aspect.ratio = 1,
  axis.ticks.y = element_blank(),
  axis.line.x = element_line(),
  axis.line.y = element_line(),
  axis.text = element_text(colour = "black", size = 6),
  legend.text = element_text(colour = "black", size = 6, family = "Helvetica")
)

breaks <- c(
  "braf", "braf_wt", "braf_wt_theta",
  "ras", "ras_wt", "ras_wt_theta",
  "egfr", "egfr_wt", "egfr_wt_theta",
  "wt", "all", "all_theta"
)


breaks_notheta <- c(
  "braf", "braf_wt",
  "ras", "ras_wt",
  "egfr","egfr_wt",
  "wt", "all"
)

ynames <- c("10% noise", "20% noise", "50% noise", "100% noise")
names(ynames) <- c(0.1, 0.2, 0.5, 1)

cols <- c(RColorBrewer::brewer.pal(6, "Paired"), "gray", "black")
names(cols) <- breaks_notheta

clabs <- c(
  "BRAFmut only",  "BRAFmut + WT",
  "RASmut only", "RASmut + WT",
  "EGFRmut only", "EGFRmut + WT",
  "Wt only", "All lines combined"
)
clabs_notheta <- clabs
names(clabs) <- breaks
names(clabs_notheta) <- breaks_notheta

ynames <- c("10% noise", "20% noise", "50% noise", "100% noise")
names(ynames) <- c(0.1, 0.2, 0.5, 1)


cols <- c(RColorBrewer::brewer.pal(6, "Paired"), "gray", "black")
names(cols) <- breaks

cols_notheta <- cols
names(cols_notheta) <- breaks_notheta

# Load and prepare the data ####
df <- read_tsv(here("../results/solutions/noise_roc_data.tsv")) %>%
  mutate(group = str_c(panel, noise, sep = "_")) %>%
  filter(fpr < 0.2)


# Fit the curves per group

df_lst <- split(df, df$group)


add_fit <- function(df) {
  yhat <- predict.scam(scam(tpr ~ s(fpr, k = 10, bs = "mpi"), data = df), se = TRUE)
  df$fit <- yhat$fit
  df$se <- yhat$se.fit
  df
}

df_fit <- bind_rows(map(df_lst, add_fit)) %>%
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
    theta = str_detect(panel, "theta"),
    color = str_replace(panel, "_theta", "")
  )


# Plot BRAFmut ROC curve ####

# Using theta = 0
df_braf <- filter(df_fit, (panel %in% c("braf_wt", "braf", "wt")) & noise == 0.1 & theta == FALSE)

p_braf <- ggplot(df_braf, aes(x = fpr, y = tpr)) +
  geom_jitter(aes(color = panel), width = 0.0025, size = 1) +
  geom_line(aes(x = fpr, y = fit, color = panel), size = 0.5) +
  geom_ribbon(
    aes(ymin = fit - se, ymax = fit + se, group = panel),
    alpha = 0.2, linetype = 2, size = 0.5) +
  scale_x_continuous(expand = c(-0.0025, 0.0025), limits = c(0, 0.2)) +
  scale_y_continuous(expand = c(-0.0025, 0.0025)) +
  geom_abline(intercept = 0, slope = 1, color = "gray", linetype = 2) +
  scale_color_manual(
    values = cols_notheta, labels = clabs_notheta, breaks = breaks_notheta, name = ""
  ) +
  labs(x = "False positive rate", y = "True positive rate") +
  use_theme +
  theme(
    text = element_text(colour = "black", size = 4, family = "Helvetica"),
    axis.title = element_text(colour = "black", size = 6, family = "Helvetica"),
    axis.text = element_text(colour = "black", size = 4),
    legend.text = element_text(colour = "black", size = 4, family = "Helvetica"),
    # axis.text.x = element_text(angle = -90, vjust = 0.5, size = 6),
    legend.position = "bottom", #c(0.85, 0.15),
    legend.key = element_rect(fill = "transparent", colour = "transparent", size = unit(1, "line")),
    legend.key.size = unit(0.5, "line"),
    legend.margin =  margin(0, 0, 0, 0, "lines")
  ) +
  guides(colour = guide_legend(override.aes = list(linetype = c(0, 0, 0))))
p_braf


# Plot all ROC curves ####

p_all <- ggplot(
  df_fit,
  aes(x = fpr, y = tpr, color = color, shape = theta)
  ) +
  facet_grid(noise ~ plot_group, labeller = labeller(noise = ynames)) +
  geom_line(aes(x = fpr, y = fit, group = panel, linetype = theta), size = 0.25) +
  geom_ribbon(aes(ymin = fit - se, ymax = fit + se), alpha = 0.2, linetype = "blank") +
  geom_jitter(width = 0.0025, size = 1) +
  scale_color_manual(
    values = cols_notheta,
    labels = clabs_notheta,
    breaks = breaks_notheta,
    name = ""
    ) +
  scale_shape_manual(
    values = c(1, 2),
    labels = c(bquote(theta == .(0)), bquote(theta == .(0.001))),
    name = ""
    ) +
  scale_linetype_manual(
    values = c("solid", "dashed"),
    labels = c(bquote(theta == .(0)), bquote(theta == .(0.001))),
    name = "",
    guide = FALSE
    ) +
  geom_abline(intercept = 0, slope = 1, color = "gray", linetype = 2) +
  scale_x_continuous(expand = c(-0.0025, 0.0025), limits = c(0, 0.2)) +
  scale_y_continuous(expand = c(-0.0025, 0.0025)) +
  labs(x = "False positive rate", y = "True positive rate") +
  theme(
    text = element_text(colour = "black", size = 10, family = "Helvetica"),
    axis.text.x = element_text(angle = -90, vjust = 0.5, size = 8),
    legend.position = "bottom"
  ) +
  guides(
    color = guide_legend(override.aes = list(fill = NA)),
    shape = guide_legend(ncol = 1)
    )
p_all
