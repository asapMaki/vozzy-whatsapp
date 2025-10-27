#!/bin/bash

# Script za kreiranje sedmičnih foldera sa dnevnim strukturama
# Sedmica: ponedjeljak - nedjelja (7 dana)
# Korištenje: ./create_weekly_structure.sh "27.10 - 02.11"
# ili: ./create_weekly_structure.sh (koristi trenutnu sedmicu)

BASE_DIR="gastrohem whatsapp"

# Funkcija za dobijanje trenutne sedmice (ponedjeljak do nedjelja)
get_current_week() {
    # Trenutni datum
    TODAY=$(date +%Y-%m-%d)

    # Dan u sedmici (1=ponedeljak, 2=utorak, ..., 7=nedjelja)
    DAY_OF_WEEK=$(date +%u)

    # Početak sedmice (ponedeljak)
    if [ $DAY_OF_WEEK -eq 1 ]; then
        # Danas je ponedeljak, to je početak sedmice
        WEEK_START=$(date +%d.%m)
    else
        # Idi nazad do ponedeljka
        DAYS_TO_MONDAY=$((DAY_OF_WEEK - 1))
        WEEK_START=$(date -v-${DAYS_TO_MONDAY}d +%d.%m)
    fi

    # Kraj sedmice (nedjelja)
    DAYS_TO_SUNDAY=$((7 - DAY_OF_WEEK))
    WEEK_END=$(date -v+${DAYS_TO_SUNDAY}d +%d.%m)

    echo "$WEEK_START - $WEEK_END"
}

# Funkcija za generisanje svih datuma u sedmici
# Argumenti: start_date (DD.MM), end_date (DD.MM), year
generate_week_dates() {
    local start_date=$1
    local end_date=$2
    local year=$(date +%Y)

    # Parse start date
    local start_day=${start_date%.*}
    local start_month=${start_date#*.}

    # Convert to YYYY-MM-DD format for date calculations
    local current_date="$year-$start_month-$start_day"

    # Generate 7 days (Monday to Sunday)
    for i in {0..6}; do
        if [ $i -eq 0 ]; then
            echo $(date -j -f "%Y-%m-%d" "$current_date" +%d.%m)
        else
            echo $(date -j -v+${i}d -f "%Y-%m-%d" "$current_date" +%d.%m)
        fi
    done
}

# Provjeri da li je proslijeđen argument za sedmicu
if [ -z "$1" ]; then
    WEEK_DIR=$(get_current_week)
    echo "Nema proslijeđene sedmice, koristim trenutnu: $WEEK_DIR"
else
    WEEK_DIR="$1"
    echo "Koristim proslijeđenu sedmicu: $WEEK_DIR"
fi

# Parsiranje početka i kraja sedmice
WEEK_START=$(echo "$WEEK_DIR" | cut -d' ' -f1)
WEEK_END=$(echo "$WEEK_DIR" | cut -d' ' -f3)

echo "Start: $WEEK_START, End: $WEEK_END"

# Automatski detektuj sve odjele u gastrohem whatsapp direktoriju
DEPARTMENTS=()
shopt -s nullglob
for dept_path in "$BASE_DIR"/*; do
    if [ -d "$dept_path" ]; then
        dept_name=$(basename "$dept_path")
        DEPARTMENTS+=("$dept_name")
    fi
done
shopt -u nullglob

echo ""
echo "========================================="
echo "Kreiranje sedmične strukture: $WEEK_DIR"
echo "Ponedjeljak - Nedjelja (7 dana)"
echo "========================================="
echo ""

# Generiši sve datume u sedmici
echo "📅 Generiši datume..."
WEEK_DATES=($(generate_week_dates "$WEEK_START" "$WEEK_END"))

echo "Datumi za kreiranje:"
for date in "${WEEK_DATES[@]}"; do
    echo "   - $date"
done
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
        echo "📁 Sedmica već postoji: $dept/$WEEK_DIR"
    else
        mkdir -p "$WEEK_PATH"
        echo "✅ Kreiran sedmični folder: $dept/$WEEK_DIR"
    fi

    # Kreiraj dnevne foldere sa chat.md fajlovima
    CREATED_COUNT=0
    for day_date in "${WEEK_DATES[@]}"; do
        DAY_PATH="$WEEK_PATH/$day_date"
        CHAT_FILE="$DAY_PATH/chat.md"

        # Kreiraj dnevni folder
        if [ ! -d "$DAY_PATH" ]; then
            mkdir -p "$DAY_PATH"
            echo "   ✅ Dan: $day_date"
            ((CREATED_COUNT++))
        else
            echo "   ℹ️  Dan već postoji: $day_date"
        fi

        # Kreiraj chat.md ako ne postoji
        if [ ! -f "$CHAT_FILE" ]; then
            # Kreiraj osnovni template za chat.md
            cat > "$CHAT_FILE" << EOF
# Chat - $day_date

## Razgovori

<!-- Razgovori za ovaj dan -->

EOF
            echo "      📝 Kreiran: chat.md"
        else
            echo "      ℹ️  chat.md već postoji"
        fi
    done

    if [ $CREATED_COUNT -gt 0 ]; then
        echo "   ✅ Kreirano $CREATED_COUNT novih dana"
    fi

    echo ""
done

echo "========================================="
echo "✅ Završeno!"
echo "========================================="
echo ""
echo "Struktura:"
echo "  gastrohem whatsapp/{odjel}/$WEEK_DIR/"
echo "    ├── ${WEEK_DATES[0]}/"
echo "    │   └── chat.md"
echo "    ├── ${WEEK_DATES[1]}/"
echo "    │   └── chat.md"
echo "    ├── ..."
echo "    └── ${WEEK_DATES[6]}/"
echo "        └── chat.md"
echo ""
