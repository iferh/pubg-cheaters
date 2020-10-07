import matplotlib.pyplot as plt
import statistics


def main():
    pass


def plot_victim_cheater_motifs(motifs_alt_univ, motifs_actual):
    '''
    Plots the victim-cheater motifs of alternative data vs the actual data.
    Takes as arguments a list of the victim-cheater motifs of the alternative
    universes as integers, and an integer of the v-c motifs for actual data.
    Returns a bar plot of the victim-cheater motifs.
    '''

    # Make variables to plot
    x = [i for i in range(len(motifs_alt_univ))]
    y = motifs_alt_univ
    names_alt_univ = ["Universe_{0}".format(i) for i in
                      range(1, len(motifs_alt_univ) + 1)]

    # Set theme for plot
    fig, ax1 = plt.subplots(figsize = (11, 8))
    ax1.set_title('Victim–cheater motifs in randomized universes')
    plt.xlabel('Number of victim–cheater motifs')
    xlen = max(motifs_alt_univ) + max(motifs_alt_univ)/3
    ax1.set_xlim([0, xlen])
    ax1.xaxis.grid(True, linestyle = '--', which = 'major',
               color = 'grey', alpha = 0.25)

    # Make vertical line for number of victim-cheater motifs in actual data:
    line_actual = ax1.axvline(motifs_actual, color = 'red', alpha = 0.99,
                              label = 'Actual Data')
    bbox_props = dict(boxstyle="round", fc = "red", lw = 1)
    text_actual = ax1.text(x = motifs_actual, y = 0.5, s = motifs_actual,
                           ha = "center", va = "center", size = 12,
                           bbox = bbox_props)

    # Make horizontal bars for every Alt-Universe:
    bars = plt.barh(x, y, align = 'center', height = 0.80,
                    tick_label = names_alt_univ,
                    label = 'Alt-universes')

    # Make a summary of the Alt-Universe data:
    alt_mean = statistics.mean(motifs_alt_univ)
    alt_median = statistics.median(motifs_alt_univ)
    alt_max = max(motifs_alt_univ)
    alt_min = min(motifs_alt_univ)
    stats = [alt_mean, alt_median, alt_max, alt_min]
    text_summ = "Summary Alt-Universe\nMean:{0}\nMedian:{1}\nMax:{2}\nMin:{3}"
    bbox_props2 = dict(boxstyle = "round", fc = "white", lw = 1)
    summary_alt = ax1.text(x = xlen - 1, y = 0,
                           s = text_summ.format(*stats), ha = "right",
                           va = "center", size = 11, bbox = bbox_props2)

    # Write labels of num of victim-cheater motifs inside each bar:
    for bar, value in zip(bars, motifs_alt_univ):
        width = int(bar.get_width())
        yloc = bar.get_y() + bar.get_height() / 2
        label = ax1.annotate(value, xy = (width-3, yloc), color = "white",
                             weight = 'bold', clip_on = True)

    # Make a legend and show
    plt.legend(loc = 1)
    plt.show()


if __name__ == '__main__':
    main();
