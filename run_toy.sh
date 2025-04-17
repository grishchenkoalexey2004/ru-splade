# don't forget to activate mamba env!
export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="config_default.yaml"
python3 -m splade.all \
  config.checkpoint_dir=experiments/debug/checkpoint \
  config.index_dir=experiments/debug/index \
  config.out_dir=experiments/debug/out
