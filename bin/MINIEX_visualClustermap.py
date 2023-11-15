import pandas, seaborn, sys

CELLID=sys.argv[1]
REGULONS=sys.argv[2]

OUT_FIG=sys.argv[3]

cellTyp_mtx = {}
for line in open(CELLID):
    cellTyp_mtx[str(line.rstrip().rsplit('\t')[0])]=line.rstrip().rsplit('\t')[1]

dic={}
with open(REGULONS) as f:
    for line in f:
        spl=line.rstrip().rsplit('\t')
        if cellTyp_mtx[spl[1].replace('Cluster_','')]+'_'+spl[1] in dic:
            dic[cellTyp_mtx[spl[1].replace('Cluster_','')]+'_'+spl[1]]+=[{spl[0]:len(spl[2].rsplit(','))}]
        else:
            dic[cellTyp_mtx[spl[1].replace('Cluster_','')]+'_'+spl[1]]=[{spl[0]:len(spl[2].rsplit(','))}]


for ele in dic:
    dic[ele]={k: v for d in dic[ele] for k, v in d.items()}

dic=pandas.DataFrame(dic).fillna(0)
dic = dic.reindex(sorted(dic.columns), axis=1) #sort columns

pal = seaborn.color_palette('Spectral_r', len(list(set(cellTyp_mtx.values()))))
colors=pal.as_hex()
celltypes=sorted(list(set(cellTyp_mtx.values())))
col_dic=dict(zip(celltypes, colors))

col_colors=[]
for c in dic.columns:
    col_colors.append([c,col_dic[c.rsplit('_')[0]]])
col_colors=pandas.DataFrame(col_colors,columns=['cluster','cell type'])

col_colors=col_colors.set_index('cluster')
seaborn.set_style('white')

def get_x_font_size_for_heatmap(dataframe):
    font_size = None
    if len(dataframe.columns) > 20:
        font_size = 5
    else:
        font_size = 7
    return font_size

def get_y_font_size_for_heatmap(dataframe):
    font_size = None
    if len(dataframe) > 300:
        font_size = 5
    elif len(dataframe) > 100:
        font_size = 5
    elif len(dataframe) > 20:
        font_size = 8
    else:
        font_size = 12
    return font_size

ax=seaborn.clustermap(dic,cmap='mako_r',yticklabels=False,xticklabels=True,col_colors=col_colors)
ax.ax_cbar.set_title('#TGs')

ax1 = ax.ax_heatmap

###reduce size of heatmap and rotate labels
heatmap_pos = ax.ax_heatmap.get_position()
ax.ax_heatmap.set_position([heatmap_pos.x0, heatmap_pos.y0, heatmap_pos.width*0.25, heatmap_pos.height])
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, horizontalalignment='right', fontsize=get_x_font_size_for_heatmap(dic))

###move color box columns down and reduce size
color_box = ax.ax_col_colors.get_position()
color_box.y0 = heatmap_pos.y0
color_box.y1 = color_box.y0 - 0.013
ax.ax_col_colors.set_position(color_box)
ax.ax_col_colors.set_position([color_box.x0, color_box.y0, color_box.width*0.25, color_box.height])

ax.ax_col_colors.tick_params(right=False) 
ax.ax_col_colors.set_yticklabels('')

###move dendogram and reduce size
dendro_box = ax.ax_col_dendrogram.get_position()
diff_dendro=dendro_box.y1-dendro_box.y0
dendro_box.y0 = heatmap_pos.y1
dendro_box.y1 = dendro_box.y0+diff_dendro
ax.ax_col_dendrogram.set_position(dendro_box)
ax.ax_col_dendrogram.set_position([dendro_box.x0, dendro_box.y0, dendro_box.width*0.25, dendro_box.height])


ax.savefig(OUT_FIG)

