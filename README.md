# Pip-Boy RED 1.7 – Galaxy Watch 8 Classic

## Co je nového
- Ciferník i všechny ručičky znovu vycentrované v souřadnicích (225, 225) – žádný posun celého obrázku doleva.
- Na červeném počítadle zbývajících služeb (např. **80**) je proklik.
- Klepnutí na číslo otevře samostatnou obrazovku **ZBÝVÁ HODIN** do **1. 10. 2027 v 00:00, Europe/Prague**, s hodinami, minutami a sekundami.
- Hodinový odpočet je přesný i přes letní/zimní čas a funguje bez internetu.
- AOD: tlumený ciferník s hodinovou a minutovou ručičkou, bez vteřinovky.

## Instalace – NUTNÉ DVĚ APK
Watch Face Format od Wear OS nesmí obsahovat Java/Kotlin kód. Pro spolehlivý živý hodinový odpočet proto instalujte **obě** APK do **hodinek** (ne do telefonu):

1. `watchface-debug.apk` – nový ciferník, applicationId `cz.youarefree.pipboyred7`.
2. `countdown-debug.apk` – aplikace hodinového odpočtu, applicationId `cz.youarefree.pipboy.countdown7`.

Stáhnout na [GitHub Actions](https://github.com/Kokotak1/App-apk/actions/workflows/build-apk.yml?query=branch%3Apipboy-red-aod) z nejnovějšího úspěšného běhu přes **Artifacts**, položka **pipboy-red-v1.7-two-apks-install-both**. ZIP obsahuje oba instalační soubory APK; rozbalit a instalovat přes Wear Installer 2. Po instalaci vybrat ciferník **Pip-Boy RED 1.7** a klepnout na červené číslo.

Použití z příkazové řádky: `adb install watchface-debug.apk` a `adb install countdown-debug.apk`.

Poznámka: APK jsou debug sestavení pro osobní test, nejsou to produkční Google Play balíčky. Starší ciferník 1.5 zůstane dostupný jako samostatná aplikace.

## Verze 1.7 – baterie a den v týdnu
- V pravém horním sektoru zůstává Vault Boy, červená 80 otevírá hodinový odpočet.
- V zeleném kovovém terminálu vlevo dole: živý údaj **[BATTERY_PERCENT]** (baterie samotných hodinek), 5 segmentů po 20 %.
- Datum nyní obsahuje také lokalizovanou zkratku dne v týdnu z **[DAY_OF_WEEK_S]**.
- Podoba hodinových a minutových ručiček, AOD a termín 1. 10. 2027 zůstávají zachované.
- Nové unikátní applicationIds pro oba balíčky kvůli kompatibilitě instalace debug APK bez konfliktu podpisů.
- Toto sestavení zachovává styl předlohy. Foto-ilustrace není doslova rastrový podklad, protože čas, baterie a datum zůstávají živé.

## Oprava 1.8: bez ikonky zámku
- Odstraněna přidaná ikona zámku z pozice 12 na ciferníku; původní grafika ciferníku zůstává.
- Červená 80, zelená baterie, den v týdnu, analogové ručičky, živé datum, AOD a proklik na hodinový odpočet zůstávají beze změny.
- Ciferník má nové `applicationId` `cz.youarefree.pipboyred8`, aby se dal nainstalovat vedle starého debug sestavení, bez konfliktu podpisu. Už nainstalovanou aplikaci hodinového odpočtu `cz.youarefree.pipboy.countdown7` není nutné instalovat znovu.


## Verze 1.9 – odolnější AOD
- AOD podklad je první, vždy viditelná vrstva; při běžném používání jej zakrývá plný barevný ciferník. Když přejde displej do ambientního režimu, barevný podklad zmizí, AOD vrstva ale zůstane.
- Hodinová a minutová ručička jsou v AOD zachované; vteřinová ručička je vypnutá.
- Baterie se počítá živě: 48 % znamená 2 z 5 segmentů (40 a 60 % jsou prahy pro druhý/třetí segment). Barevné segmenty se v AOD schovají kvůli spotřebě.
- Ostatní vzhled a kliknutí na červenou 80 zachované.
- AOD může být vypnuté operačním systémem, například když hodinky nejsou na ruce nebo se zapne úsporný režim; tuto situaci ciferník nemůže obejít.
- Nové ID ciferníku `cz.youarefree.pipboyred9`; aplikace hodinového odpočtu zůstává `cz.youarefree.pipboy.countdown7`.


## Verze 2.0 – úsporný režim baterie
- V aktivním režimu se vteřinová ručička posouvá po jedné sekundě namísto 15 Hz plynulého pohybu; WFF `Tick duration=0.05`.
- V AOD zůstávají hodinová a minutová ručička, ale s průhledností 110/255. Vteřinovka je vypnutá.
- Středová krytka v AOD je tlumená, příchozí texty/počet služeb a datum zůstávají.
- Podklad AOD je černý; původní zelený ciferník se zobrazí pouze při probuzení.
- Baterie 48 % = 2/5 segmentů, živý údaj v procentech zůstává.
- Pouze ciferník se nově instaluje jako `cz.youarefree.pipboyred20`; odpočet `cz.youarefree.pipboy.countdown7` není třeba znovu instalovat.
- Výsledná výdrž se liší podle jasu, zapnutí AOD, LTE, GPS, notifikací a dalších funkcí hodinek; úsporu je potřeba změřit na zařízení.

## Verze 2.1 ECO – kontrolní varianta při nadměrném vybíjení
- **Bez vteřinové ručičky:** hodinová i minutová ručička zůstává živá, nejsou nutné žádné sekundové tiky.
- Ilustrace je o 23 % tmavší, aby aktivní OLED podklad spotřeboval méně energie; data včetně počítadla služeb zůstávají ostrá.
- AOD grafická vrstva se při aktivním ciferníku nevykresluje (alpha=0). Uživateli, který má AOD úplně vypnuté, AOD sama o sobě vybíjení nezpůsobuje.
- Zachovány: Vault Boy, červená živá 80 s proklikem, živé procento a segmenty baterie, den v týdnu, datum a samostatný hodinový odpočet.
- Diagnostické srovnání výdrže: porovnat s originálním Samsung ciferníkem za stejných podmínek. Bez zařízení nelze prokázat, zda je příčinou právě ciferník.
- Nová identita `cz.youarefree.pipboyred21eco` umožňuje paralelní instalaci s verzí 2.0; hodinový odpočet se neinstaluje znovu.

## Verze 2.2 ECO – úsporná verze s vteřinovou ručičkou
- **Vteřinová ručička je zpět**, ale místo plynulého 15Hz pohybu vykonává jeden krátký krok za sekundu (`Tick duration="0.05" strength="1.0"`).
- V AOD je vteřinovka skrytá. Uživatel má AOD vypnuté.
- Zachováno snížení jasu grafiky o 23 % oproti původnímu ciferníku a úsporné vrstvení z ECO 2.1.
- Dynamické služby po čtyřech dnech, proklik na hodinový odpočet, baterie (48 % = 2/5 segmentů), datum, den v týdnu a hodinová i minutová ručička beze změny.
- Aplikace odpočtu se **nemění**, stačí instalovat pouze nový ciferník `cz.youarefree.pipboyred22eco`.
- Nelze zaručit úsporu výdrže bez měření na hodinkách; sekundová ručička vyžaduje obnovení displeje minimálně jednou za sekundu, když je ciferník aktivní.

## Aktualizace hodinového odpočtu 1.2 – nový termín 1. 8. 2027
- Samostatná aplikace `cz.youarefree.pipboy.countdown7` odpočítává do **1. srpna 2027 v 00:00 (Europe/Prague)**, přesně i při změně letního času.
- Aktualizuje hodiny, minuty a sekundy pouze při otevřené obrazovce; v pozadí nemá naplánovanou periodickou úlohu.
- Grafika ciferníku a červené počítadlo služeb **nejsou změněny**; počítadlo služeb nadále používá dosavadní cyklus.
- Instalace nového debug APK se stejným ID může vyžadovat nejprve odinstalovat starou aplikaci odpočtu kvůli rozdílnému podpisovému certifikátu. Ciferník není třeba odinstalovat.
