# don't forget to activate mamba env!
# splade based on ai-forever/ruSbert
export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="config_vk_ru-splade-doc_max.yaml" 
  
# Get lambda_d value from command line argument
if [ -z "$1" ]; then
    echo "Error: lambda_d parameter is required"
    echo "Usage: $0 <lambda_d>"
    echo "Example: $0 0.0001" 
    exit 1
fi

# Get run/debug mode from second argument
if [ -z "$2" ]; then
    echo "Error: run mode parameter is required" 
    echo "Usage: $0 <lambda_d> <mode>"
    echo "Example: $0 0.0001 run"
    echo "         $0 0.0001 debug"
    exit 1
fi

LAMBDA_D=$1


# Set DEBUG_SPLADE based on mode argument
if [ "$2" = "debug" ]; then
    export DEBUG_SPLADE=1
    # Remove experiments folder if it exists
    rm -rf experiments # чтобы не копились модели !
    CHECKPOINT_DIR=experiments/debug_${LAMBDA_D}/checkpoint
    INDEX_DIR=experiments/debug_${LAMBDA_D}/index
    OUT_DIR=experiments/debug_${LAMBDA_D}/out
elif [ "$2" = "run" ]; then
    export DEBUG_SPLADE=0
    CHECKPOINT_DIR=models/vk_ru-splade-doc_${LAMBDA_D}/checkpoint
    INDEX_DIR=models/vk_ru-splade-doc_${LAMBDA_D}/index
    OUT_DIR=models/vk_ru-splade-doc_${LAMBDA_D}/out
else
    echo "Error: Invalid mode. Must be 'run' or 'debug'"
    exit 1
fi

# Generate random seed between 0-1000000
SEED=$((RANDOM % 1000))




if [ "${DEBUG_SPLADE}" = "1" ]; then
    python -m splade.train \
        config.checkpoint_dir=$CHECKPOINT_DIR \
        config.index_dir=$INDEX_DIR \
        config.out_dir=$OUT_DIR \
        config.regularizer.FLOPS.lambda_q=0.0000 \
        config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
        data.VALIDATION_SIZE_FOR_LOSS=10 \
        config.record_frequency=3 \
        config.random_seed=$SEED
    exit 0
fi

if [ "${DEBUG_SPLADE}" = "0" ]; then
    python -m splade.train \
        config.checkpoint_dir=$CHECKPOINT_DIR \
        config.index_dir=$INDEX_DIR \
        config.out_dir=$OUT_DIR \
        config.regularizer.FLOPS.lambda_q=0.0000 \
        config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
        config.random_seed=$SEED 
    exit 0
fi

#! настройки регуляризатора внутри конфигурационного файла выглядят так!
# regularizer:
#     FLOPS:
#       lambda_q: 0.0000
#       lambda_d: 0.0001
#       T: 50000
#       targeted_rep: rep
#       reg: FLOPS