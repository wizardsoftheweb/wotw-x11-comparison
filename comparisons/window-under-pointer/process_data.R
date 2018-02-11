library(readr)
library(vioplot)
library(dplyr)
results <-
  read_csv(
    "./results.csv"
  )
#View(results)
#median(xcb_results$time)
#median(xlib_results$time)
xcb_results = dplyr::filter(results, library == "xcb")
xlib_results = dplyr::filter(results, library == "xlib")

gather_basics = 1000 * (xcb_results$gather_basics - xcb_results$start)
root_window = 1000 * (xcb_results$root_window - xcb_results$gather_basics)
recursion = 1000 * (xcb_results$recursion - xcb_results$root_window)
get_names = 1000 * (xcb_results$get_names - xcb_results$recursion)
parse_names = 1000 * (xcb_results$parse_names - xcb_results$get_names)
exit = 1000 * (xcb_results$exit - xcb_results$parse_names)
total = 1000 * (xcb_results$exit - xcb_results$start)

xcb_time = data.frame(gather_basics,
                      root_window,
                      recursion,
                      get_names,
                      parse_names,
                      exit,
                      total)

gather_basics = 1000 * (xlib_results$gather_basics - xlib_results$start)
root_window = 1000 * (xlib_results$root_window - xlib_results$gather_basics)
recursion = 1000 * (xlib_results$recursion - xlib_results$root_window)
get_names = 1000 * (xlib_results$get_names - xlib_results$recursion)
parse_names = 1000 * (xlib_results$parse_names - xlib_results$get_names)
exit = 1000 * (xlib_results$exit - xlib_results$parse_names)
total = 1000 * (xlib_results$exit - xlib_results$start)

xlib_time = data.frame(gather_basics,
                       root_window,
                       recursion,
                       get_names,
                       parse_names,
                       exit,
                       total)

png(
  filename = "output/violin/gather_basics.png",
  units = "px",
  width = 1000,
  height = 500,
  pointsize = 12,
  res = 96
)
vioplot(xcb_time$gather_basics,
        xlib_time$gather_basics,
        names = c('xcb', 'xlib'))
title('Violin Plot of Connection Run Time', ylab = 'Milliseconds')
dev.off()

png(
  filename = "output/violin/root_window.png",
  units = "px",
  width = 1000,
  height = 500,
  pointsize = 12,
  res = 96
)
vioplot(xcb_time$root_window,
        xlib_time$root_window,
        names = c('xcb', 'xlib'))
title('Violin Plot of Root Window Discovery Run Time', ylab = 'Milliseconds')
dev.off()

png(
  filename = "output/violin/recursion.png",
  units = "px",
  width = 1000,
  height = 500,
  pointsize = 12,
  res = 96
)
vioplot(xcb_time$recursion,
        xlib_time$recursion,
        names = c('xcb', 'xlib'))
title('Violin Plot of Window Under Pointer Discovery Run Time', ylab = 'Milliseconds')
dev.off()

png(
  filename = "output/violin/get_names.png",
  units = "px",
  width = 1000,
  height = 500,
  pointsize = 12,
  res = 96
)
vioplot(xcb_time$get_names,
        xlib_time$get_names,
        names = c('xcb', 'xlib'))
title('Violin Plot of Window Name Discovery Run Time', ylab = 'Milliseconds')
dev.off()

png(
  filename = "output/violin/parse_names.png",
  units = "px",
  width = 1000,
  height = 500,
  pointsize = 12,
  res = 96
)
vioplot(xcb_time$parse_names,
        xlib_time$parse_names,
        names = c('xcb', 'xlib'))
title('Violin Plot of Window Name Parsing Run Time', ylab = 'Milliseconds')
dev.off()

png(
  filename = "output/violin/exit.png",
  units = "px",
  width = 1000,
  height = 500,
  pointsize = 12,
  res = 96
)
vioplot(xcb_time$exit,
        xlib_time$exit,
        names = c('xcb', 'xlib'))
title('Violin Plot of Disconnection Run Time', ylab = 'Milliseconds')
dev.off()

png(
  filename = "output/violin/total.png",
  units = "px",
  width = 1000,
  height = 500,
  pointsize = 12,
  res = 96
)
vioplot(xcb_time$total,
        xlib_time$total,
        names = c('xcb', 'xlib'))
title('Violin Plot of Total Run Time', ylab = 'Milliseconds')
dev.off()

windows = sort(unique(results$window))
root_plot = data.frame(x = results$root_x,
                       y = results$root_y,
                       window = results$window)
p6 = ggplot(root_plot,
            aes(
              x = x,
              y = y,
              colour = window,
              stroke = 0
            )) +
  geom_point() +
  scale_y_reverse() +
  scale_x_continuous(position = 'top') +
  guides(colour = FALSE) +
  theme_bw()
p6
ggsave(
  'output/clicks.png',
  plot = last_plot(),
  scale = 1,
  width = 30,
  height = 20,
  units = 'cm',
  dpi = 100
)
