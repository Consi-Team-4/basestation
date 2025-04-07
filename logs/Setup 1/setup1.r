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

all_enabled <- read.table("logs/Setup 1/2025-04-06T14-32-49-472992 all enabled.csv", sep=",", col.names=col_names)
all_enabled$seconds <- all_enabled$micros / 1e6
all_enabled <- complementary_filter(all_enabled)
all_enabled <- subset(all_enabled, seconds > 78 & seconds < 86)

# plot <- ggplot(all_enabled, aes(x=seconds)) +
#     geom_line(aes(y=ax, color="X acceleration")) +
#     geom_line(aes(y=ay, color="Y acceleration")) +
#     geom_line(aes(y=az-9.81, color="Z acceleration")) +
#     geom_line(aes(y=gx, color="Roll velocity")) +
#     geom_line(aes(y=gy, color="Pitch velocity"))
# print(plot)

all_enabled_var <- apply(all_enabled, 2, var)


all_disabled <- read.table("logs/Setup 1/2025-04-06T14-49-13-814977 all disabled.csv", sep=",", col.names=col_names)
all_disabled$seconds <- all_disabled$micros / 1e6
all_disabled <- complementary_filter(all_disabled)
all_disabled <- subset(all_disabled, seconds > 53.8 & seconds < 59.8)

# plot <- ggplot(all_disabled, aes(x=seconds)) +
#     geom_line(aes(y=ax, color="X acceleration")) +
#     geom_line(aes(y=ay, color="Y acceleration")) +
#     geom_line(aes(y=az-9.81, color="Z acceleration")) +
#     geom_line(aes(y=gx, color="Roll velocity")) +
#     geom_line(aes(y=gy, color="Pitch velocity"))
# print(plot)

all_disabled_var <- apply(all_disabled, 2, var)

# # This makes a wide dataframe - bad for plotting
# variances <- data.frame(rbind(all_enabled_var, all_disabled_var))
# variances$which <- c("enabled", "disabled")

# Long dataframe - good for plotting
variances <- data.frame(which=rep(c("enabled", "disabled"), each=length(col_names)+3), var=rep(c(col_names, "seconds", "pitch", "roll"), 2), val=c(all_enabled_var, all_disabled_var))
variances <- subset(variances, var!="micros" & var!="seconds")
variances$val <- variances$val * rep(c(20, 20, 20, 1, 1, 1, 100, 100), 2)

plot <- ggplot(variances, aes(x=which, y=val, fill=var)) + geom_col(position="dodge")
print(plot)