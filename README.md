# Pip-Boy RED 1.6 – Galaxy Watch 8 Classic

## Co je nového
- Ciferník i všechny ručičky znovu vycentrované v souřadnicích (225, 225) – žádný posun celého obrázku doleva.
- Na červeném počítadle zbývajících služeb (např. **80**) je proklik.
- Klepnutí na číslo otevře samostatnou obrazovku **ZBÝVÁ HODIN** do **1. 10. 2027 v 00:00, Europe/Prague**, s hodinami, minutami a sekundami.
- Hodinový odpočet je přesný i přes letní/zimní čas a funguje bez internetu.
- AOD: tlumený ciferník s hodinovou a minutovou ručičkou, bez vteřinovky.

## Instalace – NUTNÉ DVĚ APK
Watch Face Format od Wear OS nesmí obsahovat Java/Kotlin kód. Pro spolehlivý živý hodinový odpočet proto instalujte **obě** APK do **hodinek** (ne do telefonu):

1. `watchface-debug.apk` – nový ciferník, applicationId `cz.youarefree.pipboyred6`.
2. `countdown-debug.apk` – aplikace hodinového odpočtu, applicationId `cz.youarefree.pipboy.countdown`.

Stáhnout na [GitHub Actions](https://github.com/Kokotak1/App-apk/actions/workflows/build-apk.yml?query=branch%3Apipboy-red-aod) z nejnovějšího úspěšného běhu přes **Artifacts**, položka **pipboy-red-v1.6-two-apks-install-both**. ZIP obsahuje oba instalační soubory APK; rozbalit a instalovat přes Wear Installer 2. Po instalaci vybrat ciferník **Pip-Boy RED 1.6** a klepnout na červené číslo.

Použití z příkazové řádky: `adb install watchface-debug.apk` a `adb install countdown-debug.apk`.

Poznámka: APK jsou debug sestavení pro osobní test, nejsou to produkční Google Play balíčky. Starší ciferník 1.5 zůstane dostupný jako samostatná aplikace.
