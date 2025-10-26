#!/bin/bash

# Script za čišćenje praznih dnevnih foldera u svim odjelima
# Korištenje: ./cleanup_empty_folders.sh [--dry-run]
# --dry-run: Samo prikazuje šta bi se obrisalo, bez brisanja

BASE_DIR="gastrohem whatsapp"
DRY_RUN=false

# Provjeri da li je proslijeđen --dry-run argument
if [ "$1" == "--dry-run" ]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MOD - Ništa se neće obrisati"
    echo ""
fi

# Lista svih odjela
DEPARTMENTS=(
    "administracija"
    "finansije"
    "prodaja"
    "servis"
    "svaštara"
    "sastanci menadžmenta"
    "adis-chat"
)

echo "========================================="
echo "Čišćenje praznih foldera"
echo "========================================="
echo ""

TOTAL_DELETED=0
TOTAL_FOUND=0

# Prođi kroz sve odjele
for dept in "${DEPARTMENTS[@]}"; do
    DEPT_PATH="$BASE_DIR/$dept"

    # Provjeri da li odjel postoji
    if [ ! -d "$DEPT_PATH" ]; then
        continue
    fi

    echo "📂 Odjel: $dept"
    DEPT_DELETED=0

    # Pronađi sve sedmične foldere
    shopt -s nullglob
    for week_folder in "$DEPT_PATH"/*" - "*; do
        if [ ! -d "$week_folder" ]; then
            continue
        fi

        WEEK_NAME=$(basename "$week_folder")

        # Prođi kroz sve dnevne foldere u sedmici
        for day_folder in "$week_folder"/*.[0-9][0-9]; do
            if [ ! -d "$day_folder" ]; then
                continue
            fi

            DAY_NAME=$(basename "$day_folder")

            # Provjeri da li je folder prazan (nema fajlova, samo eventualno skriveni fajlovi sistema)
            FILE_COUNT=$(find "$day_folder" -type f ! -name ".DS_Store" | wc -l | tr -d ' ')
            SUBDIR_COUNT=$(find "$day_folder" -mindepth 1 -type d | wc -l | tr -d ' ')

            if [ "$FILE_COUNT" -eq 0 ] && [ "$SUBDIR_COUNT" -eq 0 ]; then
                ((TOTAL_FOUND++))

                if [ "$DRY_RUN" = true ]; then
                    echo "   🗑️  [DRY-RUN] Bi se obrisao: $WEEK_NAME/$DAY_NAME"
                else
                    rm -rf "$day_folder"
                    echo "   ✅ Obrisan: $WEEK_NAME/$DAY_NAME"
                    ((DEPT_DELETED++))
                    ((TOTAL_DELETED++))
                fi
            fi
        done
    done

    # Provjeri da li su sedmični folderi ostali prazni nakon brisanja dnevnih
    if [ "$DRY_RUN" = false ]; then
        for week_folder in "$DEPT_PATH"/*" - "*; do
            if [ ! -d "$week_folder" ]; then
                continue
            fi

            WEEK_NAME=$(basename "$week_folder")

            # Prebroj sve stavke u sedmičnom folderu (osim .DS_Store)
            ITEM_COUNT=$(find "$week_folder" -mindepth 1 ! -name ".DS_Store" ! -name "sedmicni-summary.md" | wc -l | tr -d ' ')

            # Ako je prazan (ili samo ima sedmicni-summary.md), obriši sedmični folder
            if [ "$ITEM_COUNT" -eq 0 ]; then
                # Provjeri da li postoji samo sedmicni-summary.md
                if [ -f "$week_folder/sedmicni-summary.md" ]; then
                    SUMMARY_SIZE=$(wc -c < "$week_folder/sedmicni-summary.md" | tr -d ' ')
                    # Ako je summary prazan ili jako mali (< 50 bytes), obriši cijeli folder
                    if [ "$SUMMARY_SIZE" -lt 50 ]; then
                        rm -rf "$week_folder"
                        echo "   🗑️  Obrisan prazan sedmični folder: $WEEK_NAME"
                        ((TOTAL_DELETED++))
                    fi
                else
                    rm -rf "$week_folder"
                    echo "   🗑️  Obrisan prazan sedmični folder: $WEEK_NAME"
                    ((TOTAL_DELETED++))
                fi
            fi
        done
    fi

    if [ $DEPT_DELETED -eq 0 ] && [ "$DRY_RUN" = false ]; then
        echo "   ℹ️  Nema praznih foldera"
    fi

    echo ""
done

echo "========================================="
if [ "$DRY_RUN" = true ]; then
    echo "🔍 Pronađeno praznih foldera: $TOTAL_FOUND"
    echo "ℹ️  Pokreni bez --dry-run da ih obrišeš"
else
    echo "✅ Obrisano foldera: $TOTAL_DELETED"
fi
echo "========================================="
