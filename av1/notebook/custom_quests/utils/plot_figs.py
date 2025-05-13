def plot_hist_with_tukey(ax, data, title, color, xlabel, ylabel, use_log_scale=False):
    if data.empty:
        return  
    data_cleaned = data.dropna()
    if data_cleaned.empty:
        return
    data_cleaned.hist(bins=50, ax=ax, edgecolor="black", color=color, 
                alpha=0.7, log=use_log_scale)
    q1 = data_cleaned.quantile(0.25)
    q3 = data_cleaned.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    mean_val = data_cleaned.mean()

    ax.axvline(mean_val, color="red", linestyle='dashed', linewidth=2, label=f"Média: {mean_val:.2f}")
    ax.axvline(lower_bound, color='purple', linestyle='dashed', linewidth=2, label=f'Lim. Inf. Tukey: {lower_bound:.2f}')
    ax.axvline(upper_bound, color='purple', linestyle='dashed', linewidth=2, label=f'Lim. Sup. Tukey: {upper_bound:.2f}')
    ax.legend()

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel  + (" (Escala Log)" if use_log_scale else ""))

