#!/bin/bash

# Script za kreiranje sedmičnih foldera u svim odjelima
# Korištenje: ./create_weekly_structure.sh "20.10 - 27.10"
# ili: ./create_weekly_structure.sh (koristi trenutnu sedmicu)

BASE_DIR="gastrohem whatsapp"

# Funkcija za dobijanje trenutne sedmice (nedjelja do nedjelje)
get_current_week() {
    # Trenutni datum
    TODAY=$(date +%d.%m)
    # Dan u sedmici (0=nedjelja, 1=ponedeljak, ...)
    DAY_OF_WEEK=$(date +%u)
    # Nedjelja je 7, treba biti 0
    if [ "$DAY_OF_WEEK" == "7" ]; then
        DAY_OF_WEEK=0
    fi

    # Početak sedmice (prethodna nedjelja ili danas ako je nedjelja)
    if [ "$DAY_OF_WEEK" == "0" ]; then
        WEEK_START=$(date +%d.%m)
    else
        WEEK_START=$(date -v-${DAY_OF_WEEK}d +%d.%m)
    fi

    # Kraj sedmice (sljedeća nedjelja)
    DAYS_TO_SUNDAY=$((7 - DAY_OF_WEEK))
    WEEK_END=$(date -v+${DAYS_TO_SUNDAY}d +%d.%m)

    echo "$WEEK_START - $WEEK_END"
}

# Provjeri da li je proslijeđen argument za sedmicu
if [ -z "$1" ]; then
    WEEK_DIR=$(get_current_week)
    echo "Nema proslijeđene sedmice, koristim trenutnu: $WEEK_DIR"
else
    WEEK_DIR="$1"
    echo "Koristim proslijeđenu sedmicu: $WEEK_DIR"
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

echo ""
echo "========================================="
echo "Kreiranje sedmične strukture: $WEEK_DIR"
echo "========================================="
echo ""

# Prođi kroz sve odjele
for dept in "${DEPARTMENTS[@]}"; do
    DEPT_PATH="$BASE_DIR/$dept"
    WEEK_PATH="$DEPT_PATH/$WEEK_DIR"

    # Provjeri da li odjel postoji
    if [ ! -d "$DEPT_PATH" ]; then
        echo "⚠️  Odjel ne postoji: $dept (preskačem)"
        continue
    fi

    # Kreiraj sedmični folder
    if [ -d "$WEEK_PATH" ]; then
        echo "ℹ️  Sedmica već postoji: $dept/$WEEK_DIR"
    else
        mkdir -p "$WEEK_PATH"
        echo "✅ Kreiran folder: $dept/$WEEK_DIR"
    fi

    # Premjesti sve dnevne foldere (DD.MM format) u sedmični folder
    MOVED_COUNT=0
    shopt -s nullglob
    for day_folder in "$DEPT_PATH"/*.[0-9][0-9]; do
        # Provjeri da li folder postoji i da li je to dan (DD.MM format)
        if [ -d "$day_folder" ] && [[ $(basename "$day_folder") =~ ^[0-9]{2}\.[0-9]{2}$ ]]; then
            DAY_NAME=$(basename "$day_folder")

            # Preskoči ako je to već sedmični folder
            if [[ "$DAY_NAME" == *"-"* ]]; then
                continue
            fi

            # Preskoči ako je već u sedmičnom folderu
            if [[ "$day_folder" == *"$WEEK_DIR"* ]]; then
                continue
            fi

            # Premjesti u sedmični folder
            mv "$day_folder" "$WEEK_PATH/"
            echo "   📁 Premješten: $DAY_NAME -> $WEEK_DIR/$DAY_NAME"
            ((MOVED_COUNT++))
        fi
    done

    if [ $MOVED_COUNT -eq 0 ]; then
        echo "   ℹ️  Nema dnevnih foldera za premještanje"
    fi

    echo ""
done

echo "========================================="
echo "✅ Završeno!"
echo "========================================="
