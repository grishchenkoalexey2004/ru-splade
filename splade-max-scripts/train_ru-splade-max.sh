export PYTHONPATH=$PYTHONPATH:$(pwd)
export SPLADE_CONFIG_NAME="ru-splade-max.yaml"



# Get lambda_d value from command line argument
if [ -z "$1" ]; then
    echo "Error: lambda_d parameter is required"
    echo "Usage: $0 <lambda_d>"
    echo "Example: $0 0.0001" 
    exit 1
fi

if [ -z "$2" ]; then
    echo "Error: lambda_q parameter is required"
    echo "Usage: $0 <lambda_d> <lambda_q>"
    echo "Example: $0 0.0001 0.0001" 
    exit 1
fi

if [ -z "$3" ]; then
    echo "Error: model type parameter is required"
    echo "Usage: $0 <lambda_d> <lambda_q> <model_type>"
    echo "Example: $0 0.0001 0.0001 vk"
    echo "         $0 0.0001 0.0001 ai-forever"
    exit 1
fi

LAMBDA_D=$1
LAMBDA_Q=$2

if [ "$3" != "vk" ] && [ "$3" != "ai-forever" ]; then
    echo "Error: model_type must be either 'vk' or 'ai-forever'"
    exit 1
fi

MODEL_TYPE=$3

if [ "$MODEL_TYPE" = "vk" ]; then
    MODEL_NAME="deepvk/RuModernBERT-base"
else
    MODEL_NAME="ai-forever/ruBert-base"
fi




# Get run/debug mode from second argument
if [ -z "$4" ]; then
    echo "Error: run mode parameter is required" 
    echo "Usage: $0 <lambda_d> <lambda_q> <mode>"
    echo "Example: $0 0.0001 0.0001 run"
    echo "         $0 0.0001 0.0001 debug"
    exit 1
fi


# Set DEBUG_SPLADE based on mode argument
if [ "$4" = "debug" ]; then
    export DEBUG_SPLADE=1
    # Remove experiments folder if it exists
    CHECKPOINT_DIR=experiments/debug_${MODEL_TYPE}_${LAMBDA_D}_${LAMBDA_Q}/checkpoint
    INDEX_DIR=experiments/debug_${MODEL_TYPE}_${LAMBDA_D}_${LAMBDA_Q}/index
    OUT_DIR=experiments/debug_${MODEL_TYPE}_${LAMBDA_D}_${LAMBDA_Q}/out
elif [ "$4" = "run" ]; then
    export DEBUG_SPLADE=0
    CHECKPOINT_DIR=models/${MODEL_TYPE}_ru-splade-max_${LAMBDA_D}_${LAMBDA_Q}/checkpoint
    INDEX_DIR=models/${MODEL_TYPE}_ru-splade-max_${LAMBDA_D}_${LAMBDA_Q}/index
    OUT_DIR=models/${MODEL_TYPE}_ru-splade-max_${LAMBDA_D}_${LAMBDA_Q}/out
else
    echo "Error: Invalid mode. Must be 'run' or 'debug'"
    exit 1
fi

# Generate random seed between 0-1000000
SEED=$((RANDOM % 1000))


if [ "${DEBUG_SPLADE}" = "1" ]; then
    python -m splade.train \
        +config.checkpoint_dir=$CHECKPOINT_DIR \
        +config.index_dir=$INDEX_DIR \
        +config.out_dir=$OUT_DIR \
        config.regularizer.FLOPS.lambda_q=$LAMBDA_Q \
        config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
        data.VALIDATION_SIZE_FOR_LOSS=10 \
        config.nb_iterations=10 \
        config.record_frequency=3 \
        config.train_batch_size=4 \
        config.eval_batch_size=4 \
        +config.random_seed=$SEED \
        init_dict.model_type_or_dir=$MODEL_NAME \
        config.tokenizer_type=$MODEL_NAME
    exit 0
fi

if [ "${DEBUG_SPLADE}" = "0" ]; then
    python -m splade.train \
        +config.checkpoint_dir=$CHECKPOINT_DIR \
        +config.index_dir=$INDEX_DIR \
        +config.out_dir=$OUT_DIR \
        config.regularizer.FLOPS.lambda_q=$LAMBDA_Q \
        config.regularizer.FLOPS.lambda_d=$LAMBDA_D \
        +config.random_seed=100 \
        init_dict.model_type_or_dir=$MODEL_NAME \
        config.tokenizer_type=$MODEL_NAME
    exit 0
fi
