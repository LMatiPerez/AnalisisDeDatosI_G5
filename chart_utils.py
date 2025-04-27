def etiquetas_porcentaje_categoria(g):
    patches = []
    for i, bars in enumerate(g.containers):
        for j, bar in enumerate(bars.datavalues):
            if len(patches) <= j:
                patches.append([])
            patches[j].append(bars.datavalues[j])

    for i, bars in enumerate(g.containers):
        labels = []
        for j, _ in enumerate(bars.patches):
            p = round(patches[j][i]*100/sum(patches[j]),0)
            labels.append(f"{p:.0f}%" if p > 0 else "")
        g.bar_label(bars, labels=labels)

def etiquetas_porcentaje_total(g):
    for i, bars in enumerate(g.containers):
        labels = []
        s = sum(bars.datavalues)
        for j, bar in enumerate(bars.datavalues):
            labels.append(f"{bar*100/s:.1f}%")
        g.bar_label(bars, labels=labels)