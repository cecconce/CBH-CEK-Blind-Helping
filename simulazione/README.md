# Simulazione di fattibilità CBH — 21 novembre 2026

Simulazione software per capire se la componentistica scelta può soddisfare il requisito "cane guida": ostacoli entro 2 m, fino a 2 m di altezza e 1,5 m di larghezza.

**Esito: con la camera di profondità il sistema può funzionare; con i soli ToF + TF-Luna no.**

## Metodo
- Ray casting dei coni dei sensori contro 10 ostacoli tipo, con i sensori sul petto a 1,30 m (`cbh_cov.py`).
- Monte Carlo sui tempi di reazione, sul gradino in discesa e sull'autonomia (`cbh_sim.py`).
- Dati dei sensori di targa, non misurati: i risultati vanno confermati sul prototipo.

## Spazio d'arresto (95% dei casi)
| Velocità | Spazio d'arresto |
|---|---|
| 0,6 m/s | 0,7 m |
| 1,0 m/s (passo normale) | 1,3 m |
| 1,4 m/s (passo svelto) | 2,0 m |

Un allarme a 2 m basta fino a 1,4 m/s. Un allarme a 1,2 m (solo Modulino Distance) basta fino a circa 1,0 m/s.

## Copertura degli ostacoli
| Configurazione | Risultato |
|---|---|
| Con camera OAK-D Lite | Tutti gli ostacoli visti ad almeno 2,1 m, quindi in tempo |
| Solo 4 ToF + TF-Luna | In tempo solo il muro; persona vista a circa 1 m; paletto, sedia e cordolo mai visti |

- Palo sottile (5 cm): il ToF lo sente solo a circa 0,5 m, perché riempie poco il cono da 18°.
- Ultimo metro: la camera perde gli oggetti bassi (paletto e sedia sotto 1,15 m). Il software deve ricordare gli ostacoli già visti.
- I ToF puntati in alto e in basso portano la copertura della zona vicina dal 52% al 69–74%.

## Inclinazione della camera
| Inclinazione | Vede il pavimento da | Altezza vista a 1,3 m | Ostacoli alla testa (1,7–2 m) |
|---|---|---|---|
| Orizzontale | 2,35 m | 2,02 m | visti fino a 0,7–0,8 m |
| 15° in basso | 1,35 m | 1,62 m | persi sotto 1,6–1,75 m |

## Gradino in discesa
- La camera distingue un gradino da 10 cm solo a circa 1,0 m (tardi); uno da 15 cm a 2,1 m.
- TF-Luna puntato a terra a 1,5 m: il gradino da 10 cm produce un salto di 15 cm, contro 6 cm di rumore del sensore.
- L'oscillazione del busto di ±4° crea un falso salto di 16 cm; corretta a ±1° con l'IMU scende a 4 cm.

## Alimentazione e bus
- Consumo stimato 7–10,5 W, autonomia 6–9 h con il power bank da 72 Wh (ipotesi sui consumi di UNO Q e camera, da misurare).
- Giro I²C dei 4 ToF attraverso il Modulino Hub: circa 10 ms, non è un collo di bottiglia.

## Decisioni prese
- **OAK-D Lite**: sul petto, orizzontale.
- **TF-Luna**: puntato a terra, circa 1,5 m davanti ai piedi (inclinazione di circa 41°), in coppia con il Modulino Movement.
- **4 Modulino Distance**: due verso l'alto (circa +50°) e due verso il basso (circa −40° e −60°). Angoli di partenza, da ritoccare sul prototipo.

## Cosa la simulazione non dice
- Se la OAK-D Lite funziona sull'UNO Q (USB, container di App Lab): è il primo collaudo da fare.
- Il comportamento dei ToF al sole, su vetro e su superfici scure.
- Se la vibrazione si sente attraverso il tessuto del giubbino.

## Da misurare sul prototipo
- Consumi reali di UNO Q e camera.
- Portata dei ToF su ostacoli sottili e scuri.
- Rilevamento del gradino con TF-Luna + IMU.

## Aggiunta: piano senza camera con 3 VL53L1X (`cbh_l1x.py`)
Il referente ha tre moduli VL53L1X (cono di 27°, portata nominale 4 m). Aggiunti ai 4 Modulino Distance e al TF-Luna, senza camera. Distanza del primo allarme (in tempo se almeno 1,29 m):

| Ostacolo | Senza VL53L1X | Con 2 (12° in alto, 20° in basso) | Con 3 (22° in alto, dritto, 30° in basso) |
|---|---|---|---|
| Persona | 0,35 m | 2,10 m | 2,20 m |
| Muro | 1,50 m | 2,50 m | 2,50 m |
| Sedia/panchina 45 cm | mai | mai | 1,60 m |
| Cartello a 1,7–2,0 m | mai | mai | 1,40 m |
| Bordo tavolo 72 cm | 0,70 m | 1,45 m | 1,30 m |
| Cordolo 15 cm | 1,50 m | 1,50 m | 1,80 m |
| Transenna a 1 m | 0,40 m | 1,15 m (tardi) | 0,85 m (tardi) |
| Ramo 3 cm a 1,75 m | 0,40 m | 0,40 m | 0,90 m (tardi) |
| Palo 5 cm, paletto 60 cm | mai | mai | mai |
| **In tempo** | **2 su 10** | **4 su 10** | **6 su 10** |

- Con luce forte la portata può scendere verso 1,3 m e il vantaggio sparisce (2 su 10).
- Il sensore puntato in basso inquadra anche il pavimento: il firmware deve togliere quella lettura di fondo (non modellato).
- Conclusione: tre VL53L1X rendono il piano di riserva utilizzabile al chiuso su ostacoli grandi, ma gli ostacoli sottili e bassi restano scoperti: la camera di profondità resta necessaria per il requisito completo.

---

# Test di utilizzo simulato — 22 novembre 2026
Percorso in corridoio con 10 ostacoli, tutti i sensori (OAK-D Lite, 4 Modulino Distance, **3 VL53L1X**, TF-Luna, IMU), logica d'allarme a due livelli e tempi di reazione della persona. Dettagli, registri e script in [`test-utilizzo/`](test-utilizzo/).

| Ostacoli superati (≥ 90% delle prove) | 0,6 m/s | 1,0 m/s | 1,4 m/s |
|---|---|---|---|
| A – tutti i sensori | 9/10 | 8/10 | 8/10 |
| B – senza camera | 4/10 | 2/10 | 1/10 |

Punti critici: **vetrata** (nessun sensore la vede in tempo), **gradino** con il Luna a 1,5 m (68% a 1,0 m/s; puntandolo a 2,0 m sale al 100%), necessità di stimare il **pavimento nella camera** (altrimenti 8–22 falsi STOP al minuto).
