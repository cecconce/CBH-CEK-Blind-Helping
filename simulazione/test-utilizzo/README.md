# CBH – Simulazione di un test di utilizzo (22/11/2026)

Prototipo anno 1 con **tutti i sensori**: OAK-D Lite orizzontale, 4 Modulino Distance, **3 VL53L1X**, TF-Luna e Modulino Movement. Il feedback passa da 2 Modulino Vibro, dal Buzzer e dalle cuffie Bluetooth.
Script: `simula_test.py` (`python3 simula_test.py --n 60`, circa 7 minuti su 2 core). Variante del Luna: `variante_luna.py`. Registri delle prove: `registro_A_con_camera.txt` e `registro_B_senza_camera.txt`. Dati completi: `risultati_montecarlo.csv`.

> I dati dei sensori sono di targa o stimati, **non misurati**. La simulazione serve a scegliere cosa provare per primo sul prototipo, non a sostituire il collaudo.

## Come è fatto il test
- **Percorso**: corridoio largo 2,5 m con soffitto a 2,7 m e 10 prove. In ogni prova un ostacolo, partenza a 5 m. L'ostacolo è spostato a caso fino a ±25 cm dal centro.
- **Ostacoli**: persona, sedia scura, cartello all'altezza della testa (1,70–2,00 m), bordo di un tavolo, palo sottile (Ø 6 cm), paletto basso (70 cm), zaino a terra, vetrata, gradino in discesa (15 cm), muro.
- **Disturbi**: sole dalla finestra nelle prove della sedia e del palo; pavimento scuro nelle prove del paletto e del gradino. Il busto oscilla di ±4° a ogni passo, la quota dei sensori di ±2 cm, e l'IMU sbaglia l'angolo di circa 0,5–1°.
- **Sensori simulati con il ray casting.**
  - ToF: la portata scende con la riflettanza del bersaglio e con la porzione di cono che l'oggetto riempie. Col sole i VL53L1X arrivano a 1,3 m, i Modulino Distance a 0,8 m.
  - Camera: profondità da 0,4 a 3 m, rumore circa 1%·d², nessuna profondità sul vetro, 2% di frame persi.
  - Luna: fascio di 2°, rumore 3 cm, 5 cm su pavimento scuro.
- **Logica dell'allarme (lato Linux della UNO Q).**
  - Una lettura vale solo se si ripete due volte di fila (tre per il Luna).
  - Gli ostacoli già visti restano in **memoria** per 10 s.
  - La camera stima il pavimento a ogni frame.
  - **Allarme 1** (impulso breve + voce in cuffia) entro 2,5 m.
  - **Allarme 2 – STOP** (vibrazione continua + buzzer) alla distanza di arresto: 1,25 m a 0,6 m/s, 1,9 m a 1,0 m/s, 2,6 m a 1,4 m/s.
- **Persona**: reagisce allo STOP in 0,65 ± 0,18 s, poi frena a 1,6 ± 0,3 m/s². Una prova è **riuscita** se si ferma senza toccare l'ostacolo, contando che il piede sporge circa 35 cm davanti al petto.
- **Ripetizioni**: 60 per ogni ostacolo, a ciascuna velocità e per ciascuna configurazione. **A** = tutti i sensori; **B** = camera spenta (piano B).

## Risultati – percentuale di prove senza contatto

| Ostacolo | A 0,6 m/s | A 1,0 | A 1,4 | B 0,6 | B 1,0 | B 1,4 |
|---|---|---|---|---|---|---|
| Persona | 100% | 100% | 98% | 100% | 83% | 5% |
| Sedia (sole) | 100% | 100% | 95% | 82% | 5% | 0% |
| Cartello alla testa | 100% | 100% | 100% | 100% | 100% | 42% |
| Bordo tavolo | 100% | 100% | 97% | 75% | 0% | 0% |
| Palo sottile (sole) | 100% | 98% | 97% | 8% | 15% | 0% |
| Paletto basso (pav. scuro) | 100% | 98% | 95% | 33% | 10% | 0% |
| Zaino a terra | 100% | 100% | 98% | 67% | 27% | 0% |
| **Vetrata** | 88% | **3%** | **0%** | 85% | 7% | 0% |
| **Gradino in discesa** | 100% | **68%** | **3%** | 100% | 63% | 3% |
| Muro | 100% | 98% | 100% | 100% | 100% | 95% |
| **Ostacoli superati (≥ 90%)** | **9/10** | **8/10** | **8/10** | **4/10** | **2/10** | **1/10** |

Con la camera lo STOP parte di solito a 1,4 m a 0,6 m/s, a 2,0 m a 1,0 m/s e a 2,6–2,7 m a 1,4 m/s. Il margine che resta è di circa 0,5–0,7 m. **In quasi tutte le prove riuscite l'allarme viene dalla camera, spesso dalla sua memoria.** I ToF intervengono solo come riserva.

## Cosa emerge

1. **Con la camera il giubbino supera 8 ostacoli su 10 fino a 1,4 m/s**: tutti gli oggetti, anche bassi, sottili o scuri, e anche col sole. La camera li vede a circa 2,8 m. È il limite di 3 m messo nel modello, da verificare sul prototipo.
2. **La vetrata è il punto debole di entrambe le configurazioni.** La camera stereo non ricava profondità dal vetro. I ToF lo vedono solo a tratti e a circa 1 m, quindi l'allarme è sicuro solo camminando piano (0,6 m/s). Nota: **i sensori a ultrasuoni vedono bene il vetro**. Conviene valutare **un solo sensore a ultrasuoni puntato dritto**, solo per le superfici trasparenti (ipotesi da provare, non simulata).
3. **Il gradino in discesa arriva tardi con il Luna puntato a 1,5 m.** Lo STOP parte a circa 1,45 m: basta a 0,6 m/s, a 1,0 m/s solo nel 68% dei casi.
   Variante provata: Luna puntato a **2,0 m davanti** (inclinazione circa 33° invece di 41°). Il gradino viene preso nel **100% dei casi a 1,0 m/s** e nel **67% a 1,4 m/s**. In cambio sul pavimento scuro aumentano le false letture: fino a circa 2 STOP falsi al minuto in un campione di prova. Va trovato il compromesso sul prototipo.
4. **Stimare il pavimento dentro la camera è indispensabile.** Nella prima versione dello script il pavimento si ricavava solo dall'angolo dell'IMU: la camera dava **8–22 falsi STOP al minuto**, perché il rumore della profondità a 2–3 m «solleva» il pavimento. Con la stima del piano del pavimento a ogni frame si scende a **0–0,5 al minuto**. Quelli che restano vengono soprattutto dal Luna su pavimento scuro.
5. **Senza camera (piano B) il risultato è peggiore della simulazione del 21/11** (2 ostacoli su 10 a 1,0 m/s invece di 6). Il motivo: ora si tiene conto della riflettanza (sedia scura, zaino), della conferma su due letture e del sole. I 3 VL53L1X restano utili per il cartello alla testa e per persona e muro a passo lento. Il piano B va bene solo per una **demo a passo lento** (0,6 m/s) con ostacoli grandi e chiari.
6. **La memoria degli ostacoli funziona**: la maggior parte degli STOP parte da ostacoli visti dalla camera a 2,5–3 m e poi usciti dall'inquadratura. È il comportamento previsto per sedia, paletto e zaino nell'ultimo metro.
7. **Le frasi in cuffia** arrivano 0,25–0,4 s dopo l'allarme e sono già al livello 1, quindi la voce anticipa lo STOP. Il riconoscimento con l'IA dà frasi come «Persona a 2 metri», «Sedia a 2 metri», «Zaino a 2,5 metri». Per palo, cartello e gradino la frase è generica: «Ostacolo in alto/in basso», «Gradino in discesa».

## Bus I²C e consumi (stime)
- **I²C**: 7 ToF dietro il Modulino Hub, più Movement, 2 Vibro, Buttons e Buzzer. A 100 kHz servono circa 14 ms per giro, a 400 kHz circa 5 ms. Con i ToF a 20–30 letture al secondo il bus regge, ma conviene impostare **400 kHz**.
- **Consumi**: circa **8,4 W con camera, autonomia circa 7,3 h** con l'Anker da 20.000 mAh. Senza camera circa 4,5 W, autonomia circa 13,6 h. I consumi di UNO Q (3 W) e OAK-D Lite (3,5 W) sono ipotesi da misurare.

## Prove consigliate sul prototipo, in ordine
1. OAK-D Lite sull'UNO Q (rischio decisivo, già noto). Poi la **portata reale della profondità** su paletto e zaino: deve essere almeno 2,7 m per camminare a 1,4 m/s.
2. **Vetrata e porte a vetri**: VL53L1X dritto, e confronto con un sensore a ultrasuoni.
3. **Luna a 1,5 m e a 2,0 m** sul gradino della scuola, su pavimento chiaro e scuro, contando i falsi allarmi.
4. Stima del pavimento nella nuvola di punti della camera, da mettere nel firmware fin dall'inizio.
5. Tempi di reazione reali alla vibrazione attraverso il tessuto: nel modello 0,65 s.

## Limiti della simulazione
Ostacoli fermi e un ostacolo alla volta; nessuna persona in movimento. La persona reagisce solo allo STOP e non rallenta all'allarme 1. Il riconoscimento dell'IA è semplificato. Compatibilità camera/UNO Q, latenza reale di App Lab, vetro e sole sono modellati in modo approssimativo.
