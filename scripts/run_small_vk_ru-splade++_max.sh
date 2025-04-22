# don't forget to activate mamba env!
# splade based on ai-forever/ruSbert
export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="config_small_vk_ru-splade++_max.yaml"
python -m splade.train