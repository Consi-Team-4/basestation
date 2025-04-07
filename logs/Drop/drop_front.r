rm(list=ls())

library(ggplot2)

col_names <-  c("micros", "gx", "gy", "gz", "ax", "ay", "az")
gravity <- 9.81

drop_enabled <- read.table("logs/Drop/2025-04-06T18-23-02-306968 drop 2 enabled.csv", sep=",", col.names=col_names)
drop_enabled$seconds <- drop_enabled$micros / 1e6
enabled_start <- 1596.29
drop_enabled <- subset(drop_enabled, seconds > enabled_start & seconds < enabled_start + 1)

# plot <- ggplot(drop_enabled, aes(x=seconds)) +
#     geom_line(aes(y=az-9.81, color="Z acceleration")) +
#     geom_line(aes(y=gy, color="Pitch velocity"))
# print(plot)


drop_disabled <- read.table("logs/Drop/2025-04-06T18-22-38-199087 drop 2 disabled.csv", sep=",", col.names=col_names)
drop_disabled$seconds <- drop_disabled$micros / 1e6
disabled_start <- 1570.05
drop_disabled <- subset(drop_disabled, seconds > disabled_start & seconds < disabled_start + 1)

# plot <- ggplot(drop_disabled, aes(x=seconds)) +
#     geom_line(aes(y=az-9.81, color="Z acceleration")) +
#     geom_line(aes(y=gy, color="Pitch velocity"))
# print(plot)

plot <- ggplot() + xlab("Seconds") + ylab("Acceleration (m/s^2) or Angular Velocity (rad/s)") +
    geom_line(aes(x=seconds-enabled_start, y=az-gravity, color="Enabled: Z acceleration"), data=drop_enabled) +
    geom_line(aes(x=seconds-enabled_start, y=ax, color="Enabled: X acceleration"), data=drop_enabled) +
    geom_line(aes(x=seconds-enabled_start, y=gy, color="Enabled: Pitch velocity"), data=drop_enabled) + 
    geom_line(aes(x=seconds-disabled_start, y=az-gravity, color="Disabled: Z acceleration"), data=drop_disabled) +
    geom_line(aes(x=seconds-disabled_start, y=ax, color="Disabled: X acceleration"), data=drop_disabled) +
    geom_line(aes(x=seconds-disabled_start, y=gy, color="Disabled: Pitch velocity"), data=drop_disabled)
print(plot)