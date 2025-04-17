# don't forget to activate mamba env!
export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="config-default.yaml"
python -m splade.push_to_hf \
  config.checkpoint_dir=experiments/debug/checkpoint \
  config.index_dir=experiments/debug/index \
  config.out_dir=experiments/debug/out
