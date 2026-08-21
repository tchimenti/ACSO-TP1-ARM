set -e

cd src
make clean || true
make

echo "Compilación exitosa, continuando..."

cd ..
chmod +x .github/scripts/generate_dump.sh
.github/scripts/generate_dump.sh

TEST_FILES="./test/mandatory_test.py"

if [[ -d "custom_dumpsim" ]]; then
    echo "Carpeta custom_dumpsim detectada. Incluyendo tests personalizados..."
    TEST_FILES="$TEST_FILES ./test/custom_test.py"
fi

set +e
pytest $TEST_FILES --verbose
set -e

rm -rf mandatory_dumpsim
rm -rf extra_dumpsim
rm -rf custom_dumpsim
find ./inputs -maxdepth 1 -type f -name "*.x" -delete
cd src
make clean || true