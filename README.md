# heat_wave

Questo programma ha lo scopo di identificare e classificare le ondate di calore tra i dati raccolti da ECMWF dall' 1 gennaio 1950 al 31 dicembre 2021 nella regione Artica. Il programma si compone di due componenti: la prima ha lo scopo di identificare gli eventi ondata di calore e la seconda quello di classificare tali eventi sulla base delle anomalie di altezza geopotenziale a 500 hPa. 

Per utilizzare il programma è necessario scaricare in formato netCDF4 i seguenti dati: 
- Media dei valori di temperatura a 2m di un'intera sezione a nord di 75°N per ogni giornata considerata nello studio
- Temperatura media a 2m di un'intera sezione a nord di 30°N
- Altezza geopotenziale a 500 hPa di un'intera sezione a nord di 30°N

IDENTIFICAZIONE DEGLI EVENTI:

La parte di programma dedicata all'identificazione degli eventi è salvata con il nome read.py. All'inizio del file è presente una variabile di nome "path", dove andrà inserito il path del file netCDF4 contenente la media dei valori di temperatura a 2m (1 valore per giorno). 

esempio: 

path='/home/giulia/Documents/Documenti/Tesi/pc_TAS_daymean.nc'

Il programma si occupa di spacchettare in numpy array i dati contenuti nel file .nc e di identificare le ondate di calore sulla base di una climatologia dipendente dal tempo che considera per ogni giorno una finestra di 20 giorni per 9 anni con centro sul giorno interessato. La soglia oltre al quale una giornata è da considerarsi una giornata calda è il 90° percentile calcolato sulla climatologia sopra definita. I criteri di persistenza considerati sono un minimo di 3 giornate calde consecutive per poter identificare un'ondata di calore.

Il programma salverà un file netCDF4 per ogni anno appartenente allo studio, è necessario inserire il nome che si intende dare al file nella parte di programma:

with open("JFM_90pct_"+str(years[0]+k)+".csv", "w") as stream:

dove è stato considerato il nome JFM_90pct_ per intendere che il periodo studiato è quello invernale considerando una soglia a 90° percentile.

E' possibile selezionare il periodo dell'anno specifico o il periodo di anni di cui si intende identificare gli eventi ondate di calore. Al termine del file read.py si trova un for loop in cui inserire i vincoli temporali, esempio: 

for k in range(0,70):
    woy = warm_days_wod_y(temp_matrix, k,0,90)
    w=np.append(w,len(woy))

la funzione warm_days_wod_y() prende come argomenti: temp_matrix = la matrice di temperatura che contiene i valori di temperatura media di ogni giorno dell'anno per tutti gli anni considerati nello studio, k = l'anno di riferimento ( il range di anni di interesse è selezionato nel range(:,:) nella definizione del for loop), day_begin = giorno di inizio del periodo dell'anno di interesse, day_end = giorno di fine del periodo di interesse. Lo 0 corrisponde al 1 Gennaio di ogni anno ( ad esempio 0, 90 indica il periodo January- February- March). 

CLASSIFICAZIONE DEGLI EVENTI:



Python 100.0%
