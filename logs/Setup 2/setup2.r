rm(list=ls())

library(ggplot2)

col_names <-  c("micros", "gx", "gy", "gz", "ax", "ay", "az")
gravity <- 9.81

complementary_filter <- function(df) {
    df$pitch <- df$micros
    df$roll <- df$micros

    df$pitch[1] <- atan2(df$ax[1], df$az[1])
    df$roll[1] <- atan2(df$ay[1], df$az[1])

    for (i in 2:nrow(df)) {
        dt <- (df$seconds[i] - df$seconds[i-1])
        decay <- exp(-dt/0.2)

        df$pitch[i] <- (1-decay)*atan2(df$ax[i], df$az[i]) + decay*df$pitch[i-1] + dt*(-df$gy[i])
        df$roll[i] <- (1-decay)*atan2(df$ay[i], df$az[i]) + decay*df$roll[i-1] + dt*df$gx[i]
    }

    return(df)
}

all_enabled <- read.table("logs/Setup 2/2025-04-06T15-08-53-005173 all enabled.csv", sep=",", col.names=col_names)
all_enabled$seconds <- all_enabled$micros / 1e6
all_enabled <- complementary_filter(all_enabled)
all_enabled <- subset(all_enabled, seconds > 39.5 & seconds < 48)

# plot <- ggplot(all_enabled, aes(x=seconds)) +
#     geom_line(aes(y=ax, color="X acceleration")) +
#     geom_line(aes(y=ay, color="Y acceleration")) +
#     geom_line(aes(y=az-9.81, color="Z acceleration")) +
#     geom_line(aes(y=gx, color="Roll velocity")) +
#     geom_line(aes(y=gy, color="Pitch velocity")) +
#     geom_line(aes(y=pitch, color="Pitch")) +
#     geom_line(aes(y=roll, color="Roll"))
# print(plot)

all_enabled_var <- apply(all_enabled, 2, var)


no_lidar <- read.table("logs/Setup 2/2025-04-06T15-25-16-316221 no lidar.csv", sep=",", col.names=col_names)
no_lidar$seconds <- no_lidar$micros / 1e6
no_lidar <- complementary_filter(no_lidar)
no_lidar <- subset(no_lidar, seconds > 132 & seconds < 139)

# plot <- ggplot(no_lidar, aes(x=seconds)) +
#     geom_line(aes(y=ax, color="X acceleration")) +
#     geom_line(aes(y=ay, color="Y acceleration")) +
#     geom_line(aes(y=az-9.81, color="Z acceleration")) +
#     geom_line(aes(y=gx, color="Roll velocity")) +
#     geom_line(aes(y=gy, color="Pitch velocity"))
# print(plot)

no_lidar_var <- apply(no_lidar, 2, var)


all_disabled <- read.table("logs/Setup 2/2025-04-06T14-59-06-890147 all disabled.csv", sep=",", col.names=col_names)
all_disabled$seconds <- all_disabled$micros / 1e6
all_disabled <- complementary_filter(all_disabled)
all_disabled <- subset(all_disabled, seconds > 31 & seconds < 37)

# plot <- ggplot(all_disabled, aes(x=seconds)) +
#     geom_line(aes(y=ax, color="X acceleration")) +
#     geom_line(aes(y=ay, color="Y acceleration")) +
#     geom_line(aes(y=az-9.81, color="Z acceleration")) +
#     geom_line(aes(y=gx, color="Roll velocity")) +
#     geom_line(aes(y=gy, color="Pitch velocity"))
# print(plot)

all_disabled_var <- apply(all_disabled, 2, var)


gyro_scale = 5

# Long dataframe - good for plotting
variances <- data.frame(which=rep(c("All Enabled", "No LIDAR", "All Disabled"), each=length(col_names)+3), Variable=rep(c(col_names, "seconds", "pitch", "roll"), 3), val=c(all_enabled_var, no_lidar_var, all_disabled_var))
variances <- subset(variances, Variable!="micros" & Variable!="seconds")
variances$val <- sqrt(variances$val)
variances$val <- variances$val * rep(c(gyro_scale, gyro_scale, gyro_scale, 1, 1, 1, 1, 1), 3)

variances_raw <- subset(variances, Variable!="pitch" & Variable !="roll" & Variable !="gz")
variances_filtered <- subset(variances, Variable=="pitch" | Variable =="roll")


raw_palette <- c("#c43048", "#bd4122", "#c46527", "#164eb6", "#574de4")

plot <- ggplot(variances_raw, aes(x=which, y=val, fill=Variable)) + geom_col(position="dodge") + xlab("") + theme(text=element_text(size=24)) + scale_fill_manual(values=raw_palette) +
    scale_y_continuous(
        name="Acceleration (m/s^2)",
        sec.axis = sec_axis(transform=~./gyro_scale, name="Angular Velocity (rad/s)")
    )
print(plot)

plot <- ggplot(variances_filtered, aes(x=which, y=val, fill=Variable)) + geom_col(position="dodge") + xlab("") + theme(text=element_text(size=24)) +
    scale_y_continuous(
        name="Attitude (rad)"
    )
#print(plot)