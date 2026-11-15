# You Are Free – Galaxy Watch 8 Classic LTE

Vlastní analogový ciferník pro Samsung Galaxy Watch 8 Classic LTE. Černé pozadí, stříbrné ručičky, zelený kruh, jeden datum dole a nahoře pouze **ZBÝVÁ** plus proměnlivé zelené číslo. Žádný nápis „služeb“ ani „You Are Free“ se na ciferníku nezobrazuje.

## Počítadlo
První plánovaná služba **18. 11. 2026**, dále každé **4 dny**. Do cílového dne **1. 10. 2027** připadá 80 služeb. Počítadlo ukazuje 80 do konce dne 18. 11., následující den 79, po každé další službě se sníží o jednu a **1. 10. 2027** je 0. Výpočet používá lokální datum hodinek; změny času zima/léto ho neovlivní. Počítadlo je omezené na hodnoty 0–80.

## Projekt
Projekt používá deklarativní [Watch Face Format](https://developer.android.com/training/wearables/wff), aby fungoval na moderních hodinkách Wear OS. Žádná telefonní aplikace není potřeba. Přesné obrázky ciferníku vznikají skriptem v `tools/make_assets.py` a texty a ručičky se na hodinkách vykreslují živě.

## Sestavení bez Android Studia
V záložce [Actions](https://github.com/Kokotak1/App-apk/actions) vyberte **Build Watch Face APK** a stiskněte **Run workflow**. Po úspěšném běhu najdete instalační balíček **you-are-free-debug-apk** v sekci Artifacts. Debug APK je určen pro vlastní testování, nikoli pro vydání v Google Play. Lze jej nainstalovat pomocí ADB do hodinek s povoleným laděním. Automatický běh se spouští také při změnách zdrojového projektu.

## Stav
Zdrojový projekt, časové výpočty a sestavovací workflow jsou připravené, ale funkčnost sestavení a přesné vykreslení je třeba ověřit výsledkem GitHub Actions a na skutečných hodinkách. Obrázek návrhu není přímou bitmapou finálního ciferníku.

## Poznámka k AOD
Ciferník si nastavení Always On Display na zařízení nemůže sám vypnout. Pokud AOD nechcete, vypněte jej v nastavení Galaxy Watch.
