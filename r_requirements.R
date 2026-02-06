packages <- c(
  "tikzDevice",
  "ggplot2",
  "ggrepel",
  "rstan",
  "loo"
)

installed <- rownames(installed.packages())
to.install <- packages[which(!(packages %in% installed))]

if (length(to.install) > 0) {
  install.packages(to.install)
}