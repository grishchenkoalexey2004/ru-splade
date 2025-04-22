# don't forget to activate mamba env!
# splade based on ai-forever/ruSbert
export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="config_vk_ru-splade++_max.yaml"
python -m pdb -m splade.train