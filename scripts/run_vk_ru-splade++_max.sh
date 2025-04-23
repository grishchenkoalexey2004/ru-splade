# don't forget to activate mamba env!
# splade based on ai-forever/ruSbert
export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="config_vk_ru-splade++_max.yaml"

if [ "${DEBUG_SPLADE}" = "1" ]; then
    python -m pdb -m splade.train
    exit 0
fi

if [ -z "${DEBUG_SPLADE}" ] || [ "${DEBUG_SPLADE}" = "0" ]; then
    python -m splade.train
    exit 0
fi
