import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams.update({
 'font.family':'DejaVu Sans','font.size':8,'axes.titlesize':8.5,'axes.labelsize':8,'xtick.labelsize':7.5,'ytick.labelsize':7.5,
 'legend.fontsize':7.2,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':0.7,'xtick.major.width':0.7,'ytick.major.width':0.7,
 'figure.dpi':150,'savefig.dpi':300,'savefig.bbox':'tight','savefig.pad_inches':0.05,'axes.titleweight':'bold','axes.titlelocation':'left',
 'pdf.fonttype':42})
C=dict(M1='#1B7F8C',M2='#D98324',M3='#7A4FA3',ORACLE='#2B2B2B',thr='#C0392B',grey='#8A8F98',light='#EEF1F5',ink='#1F2933',good='#2E8B57',bad='#C0392B',blue='#2F5D8C')
LAB=dict(M1='M1 (broad-band)',M2='M2 (band-pair)',M3='M3 (band-pair + asym.)',ORACLE='Oracle (ground truth)')
def panel(ax,letter):
    ax.text(-0.02,1.08,letter,transform=ax.transAxes,fontsize=11,fontweight='bold',va='bottom',ha='right')
